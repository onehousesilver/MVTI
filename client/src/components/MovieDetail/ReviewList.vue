<template>
  <div id="ReviewList">
    <!-- <h3 class="reviewListHead" v-if="reviewCnt < 999">REVIEW ({{ reviewCnt }})</h3> -->
    <h3 class="reviewListHead" v-if="reviewCnt < 999">REVIEW ({{ propReviews.length }})</h3>
    <h3 class="reviewListHead" v-else>REVIEW (999+)</h3>

    <div class="reviewLists" v-for="review in propReviews" :key="review.id">
      <div>
        <div class="reviewProfileContainer">
          <span class="profileBg" :style="{'background-color':getColors()}"></span>
          <span class="profileCon">
            <p class="reviewUserMbti">{{ review.user.mbti }}</p>
            <p class="reviewWriter">{{ review.user.nickname }}</p>
            <p class="reviewEmail">{{ review.user.username }}</p>
            <p class="reviewStar">{{ rank[review.rank-1] }}</p>
          </span>
        </div>
        <div class="reviewContentContainer">
          <h5 class="reviewListTitle">
            <span v-if="commentToggle && review.id===reviewPk">
              <label for="reviewListUpdateTitle">수정할 제목과 내용을 입력 해 주세요</label>
              <b-form-input b-form-input id="reviewListUpdateTitle" type="text" v-model="sendData.title"></b-form-input>
            </span>
            <span v-else style="font-weight: 600;">{{ review.title }}</span></h5>
          <hr>
          <p class="reviewListContent">
            <span v-if="commentToggle && review.id===reviewPk">
              <b-form-textarea type="text" v-model="sendData.content" no-resize style="height:160px;">
              </b-form-textarea>
            </span>
            <span v-else style="font-size: 18px;">{{ review.content }}</span></p>
          <p class="reviewListRate">
            <span v-if="commentToggle && review.id===reviewPk">
              <span class="star-rating2">
                <input type="radio" id="5-starss" name="rate" value="5" v-model="rate" />
                <label for="5-starss" class="star pr-4">⭐</label>
                <input type="radio" id="4-starss" name="rate" value="4" v-model="rate" />
                <label for="4-starss" class="star">⭐</label>
                <input type="radio" id="3-starss" name="rate" value="3" v-model="rate" />
                <label for="3-starss" class="star">⭐</label>
                <input type="radio" id="2-starss" name="rate" value="2" v-model="rate" />
                <label for="2-starss" class="star">⭐</label>
                <input type="radio" id="1-starss" name="rate" value="1" v-model="rate" />
                <label for="1-starss" class="star">⭐</label>
              </span>
              <b-button pill variant="light" class="reviewListBtn reveiwModifyBtn" @click="updateReview(review)">수정하기</b-button>
              <b-button pill variant="light" class="reviewListBtn reveiwModifyBtn" @click="commentToggle = false">수정취소</b-button>
            </span></p>
            <span class="createUpdateTime">
              <p style="font-size: 14px; margin: 0px; margin-bottom: 6px">작성시간: {{ review.created_at| moment("calendar") }}</p>
              <p style="font-size: 14px;">수정시간: {{ review.updated_at| moment("calendar") }}</p>
            </span>
          
          <span v-if="!commentToggle" class="updateDeleteBtns">
            <b-button variant="outline-dark" class="reviewListBtn" @click="updateFromCreate(review)">리뷰 수정</b-button>
            <b-button variant="outline-dark" class="reviewListBtn" @click="deleteReview(review)">리뷰 삭제</b-button>
          </span>
        </div>
      </div>
      <comment-list @comment-updated="getComments" :reviewPk="review.id" :commentCnt="review.comments_count"></comment-list>
    </div>
  </div>
</template>

<script scoped>
import axios from 'axios'
import _ from 'lodash'
import CommentList from '@/components/MovieDetail/CommentList.vue'

export default {
  name:'ReviewList',
  components: {
    CommentList
  },
  data: function () {
    return {
        moviePk : this.$route.params.moviepk,
        reviewPk : null,
        commentToggle: false,
        currentUsername: null,
        rate: null,
        sendData: {
          title: '',
          content: '',
          rank: 0,
        },
        profileColorList: [
          '#FFC83D', '#01B2FF', '#FFAA2C', 
          '#FDA8C6', '#E40000', '#65E500', 
          '#210066', '#121212', '#F4F4F4',
          '#F08080'
        ],
        rank: ['⭐', '⭐⭐', '⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'],
    }
  },
  props: {
    movieInfo: Object,
    propReviews: Array,
    reviewCnt: Number, 
  },
  methods: {
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`
      }
      return config
    },
    // 리뷰 조회🕵️‍♀️
    getReviews: function () {
      axios({
      method: "get",
      url: `http://127.0.0.1:8000/movies/review/${this.moviePk}/`,
      headers: this.setToken()
      })
      .then((res) => {
        this.reviews = res.data
      })
      .catch(()=>{
        console.log('갓진석!!!갓진석!!')
      }) 
    },
    // 리뷰 삭제😟
    deleteReview: function (review) {
      axios({
      method: "delete",
      url: `http://127.0.0.1:8000/movies/review/change/${review.id}/`,
      headers: this.setToken()
      })
      .then(() => {
        this.$emit('review-updated')
      })
    },
    // 댓글 폼 생성👀
    updateFromCreate: function (e) {
      // 만약 내가 쓴 글이면 클릭한 댓글의 수정창만 보이게하기
      this.sendData.title = e.title
      this.sendData.content = e.content
      this.reviewPk = e.id
      // 내가 쓴 글인지 확인하는 if
      if (e.user.username === this.currentUsername) {
        this.commentToggle = !this.commentToggle
      } else {
        alert('다른 사람이 작성한 글은 수정할 수 없습니다.')
      }
    },
    // 리뷰 수정🤔
    updateReview: function (review) {
      // console.log('rate',this.rate)
      this.sendData.rank = this.rate
      axios({
      method: "put",
      url: `http://127.0.0.1:8000/movies/review/change/${review.id}/`,
      headers: this.setToken(),
      data: this.sendData,
      })
      .then(() => {
        this.sendData.title = ''
        this.sendData.content = ''
        this.sendData.rank = ''
        this.$emit('review-updated')
        this.commentToggle = false
      })
    },
    // 코멘트 개수 전달
    getComments: function () {
      // console.log('comment 개수 prop하는거 다시 주기')
    },
    getColors: function () {
      return _.sample(this.profileColorList)
    },
  },
  created: function () {
    // 현재 접속자 정보 가져오기(내가 쓴 댓글만 수정할 수 있게)
    axios({
      method: "get",
      url: 'http://127.0.0.1:8000/accounts/profile/',
      headers: this.setToken()
    })
    .then((res) => {
        this.currentUsername = res.data.username
      })
    .catch(()=>{
      console.log('리뷰 username 가져오다 난 에러')
    })
  },
  updated: function () {
    this.getReviews()
  },
  watch: {
  },
}
</script>

<style scoped>
button {
  font-size: 16px;
  z-index: 100;
}
label {
  font-size: 16px;
}
.star {
  font-size: 24px;
}

#ReviewList {
  margin: 0 auto;
  width: 100%;
  max-width: 1200px;
  text-align: left;
  /* border: 1px solid black; */
}
.reviewListHead {
  font-weight: 700;
  margin-bottom: 30px;
}

.reviewProfileContainer {
  float: left;
  width: 32%;
  padding: 30px;
}
.profileBg {
  display: block;
  width: 60px;
  height: 60px;
  border-radius: 60px;
  overflow: hidden;
  background: center / contain no-repeat url('../../assets/profile_default.png');
  background-size: 50px;
  background-position-y: 10px;
  float: left;
}
.profileCon {
  float: left;
  margin-left: 30px;
}
.profileCon p {
  margin-bottom: 0;
}
.profileCon .reviewUserMbti {
  font-size: 15px;
  font-weight: 500;
  padding-left: 6px;
}
.profileCon .reviewWriter {
  font-size: 20px;
  font-weight: 700;
  padding-left: 3px;
}
.profileCon .reviewEmail {
  font-size: 12px;
  padding-left: 3px;
  color: rgb(168, 168, 168);
}
.profileCon .reviewStar {
  font-size: 26px;
  margin-top: 4px;
}


.reviewLists {
  border-radius: 10px;
  margin-bottom: 28px;
  backdrop-filter: blur(10px);
  background-color: #f8f9fa;
  border: 1px solid rgba(0,0,0,.125);
  padding-bottom: 10px;
}

.reviewContentContainer {
  padding: 30px;
  float: left;
  width: 68%;
  /* background: lightsteelblue; */
}

.reveiwModifyBtn {
  float: right;
}

.createUpdateTime {
  float: left;
  margin-top: 30px;
}

.updateDeleteBtns {
  float: right;
  margin-top: 30px;
}
.updateDeleteBtns button:first-child {
  margin-right: 12px;
}

.reviewListUpdateTitle {
  font-weight: 700;
}

/* /////////////////////////////////////////////////// */
.star-rating2 {
  margin: 0px 0px 0px 10px;
  display:flex;
  flex-direction: row-reverse;
  font-size:1.5em;
  justify-content:space-around;
  text-align:center;
  width:5em;
  /* border: 1px solid red; */
  margin-left: 20px;
}
.star-rating2 input {
  display:none;
}
.star-rating2 label {
  cursor:pointer;
  filter: grayscale(100%);
}
.star-rating2 :checked ~ label {
  filter: grayscale(0);
}
.star-rating2 label:hover,
.star-rating2 label:hover ~ label {
  filter: grayscale(0);
}
</style>