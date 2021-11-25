<template>
  <div id="Profile">
    <!-- 카드플필 -->
    <div class="cardProfile">
      <h2 style="font-weight: 700; text-align: left; ">프로필</h2>
      <div class="profileContainer">
        <div class="profile" :style="{'background':profileColor}">
          <img src="@/assets/profile_default.png" alt="">
        </div>
      </div>
      <b-card-text class="nickname">
        <span style="float: left;">{{ nickname }}({{ username }}) 회원님의 <b>MBTI</b>는 <b v-show="MBTI">{{ MBTI }}</b><b v-show="!MBTI">----</b>입니다.</span><br><br>
        <div style="width: 100px; height: 100px; float: left; font-size: 16px; padding: 6px; margin: 0 30px 0 10px; ">
          작성한 리뷰 <span style="font-size: 40px;">{{ myReviewsTotal }}</span>개</div>
        <div style="width: 100px; height: 100px; float: left; font-size: 16px; padding: 6px;">
          내 영화 <br><span style="font-size: 40px;">{{ myListsTotal }}</span>개</div>
        <div v-if="isAdmin" style="width: 100px; height: 100px; float: left; font-size: 16px; padding: 6px;">
        장르 DB <br><span @click="getGenreDB" style="font-size: 40px; cursor: pointer;">🦸‍♀️</span></div>
        <div v-if="isAdmin" style="width: 100px; height: 100px; float: left; font-size: 16px; padding: 6px;">
        영화 DB <br><span @click="getMovieDB" style="font-size: 40px; cursor: pointer;">🎬</span></div>
      </b-card-text>
    </div>

    <!--내 영화 리스트 토글-->
    <div class="mb-3">
      <span>
      <h3 style="font-weight: 700; text-align: left;">내 영화 리스트</h3>
      <b-button v-if="myLists" class="b-button" v-b-toggle.my-collapse @click="expandMyList">펼쳐보기 <b-icon icon="caret-down-fill"></b-icon></b-button>
      <!-- <b-button v-if="myLists" class="b-button" v-b-toggle.my-collapse>펼쳐보기 <b-icon icon="caret-down-fill"></b-icon></b-button> -->
      <div v-else style="float: left; width: 100%; margin-top: 20px; font-weight: 400; font-size: 20px;">아직 내 영화가 없어요😥</div>
      </span>

      <!-- <b-collapse id="my-collapse">
        <b-card>I am collapsible content!</b-card>
      </b-collapse> -->

      <span v-show="!toggleMyList" class="myMovieList deactive">
        <div class="myMoviePoster" v-for="(myMovie, index) in myLists" :key="index">
          <span class="posterContainer">
            <img :src="myMovie.poster_path" alt=""
            @click="$router.push({ name: 'MovieDetail', params: { moviepk: myMovie.movie }})" style="cursor:pointer;">
          </span>
        </div>
      </span>

      <span v-show="toggleMyList" class="myMovieList">
        <div class="myMoviePoster" v-for="(myMovie, index) in myLists" :key="index">
          <span class="posterContainer">
            <img :src="myMovie.poster_path" alt=""
            @click="$router.push({ name: 'MovieDetail', params: { moviepk: myMovie.movie }})" style="cursor:pointer;">
          </span>
        </div>
      </span>
    </div>

    <!--리뷰-->
    <div id="my-review">
      <h3>내가 쓴 리뷰</h3>
      <div class="writed-reviews" v-for="review in myReviews" :key="review.id" @click="detailFromReview(review.movie)">
        <span class="my-review-movie"> {{ review.movie_title }} </span>
        <span class="my-review-title"> {{ review.title }} </span>
        <span class="my-review-content"> {{ review.content }} </span>
        <span class="my-review-updated"> {{ review.updated_at | moment('YYYY-MM-DD HH:mm:ss') }}</span>
      </div>
      
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import _ from 'lodash'
// import MyReview from '@/components/Profile/MyReview.vue'

export default {
  name: 'Profile',
  components: {
    // MyReview,
  },
  data: function () {
      return {
        userPK: null,
        username: null,
        nickname: null,
        MBTI: null,
        myReviews: null,
        myReviewsTotal: null,
        myPosters: null,
        myLists: null,
        myListsTotal: null,
        myTest: null,
        profileColor: '',
        profileColorList: [
          '#FFC83D', '#01B2FF', '#FFAA2C', 
          '#FDA8C6', '#E40000', '#65E500', 
          '#210066', '#121212', '#F4F4F4',
          '#F08080'
        ],
        toggleMyList: false,
        isAdmin: false,
      }
  },
  methods: {
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`
      }
      return config
    },
    // 프로필 컬러 랜덤🎨
    getColors: function () {
      return _.sample(this.profileColorList)
    },
    detailFromReview: function (moviePK) {
      this.$router.push({ name: 'MovieDetail', params: { moviepk: moviePK }})
    },
    expandMyList: function() {
      this.toggleMyList = !this.toggleMyList
    },
    getGenreDB: function () {
      axios({
          method: 'post',
          url: `http://127.0.0.1:8000/movies/db/genres/`,
          headers: this.setToken(),
        })
        .then(()=> {
        })
        .catch(() => {
          this.$swal('error', '관리자 권한이 없습니다', 'error');
      })  
    },
    getMovieDB: function () {
      axios({
          method: 'post',
          url: `http://127.0.0.1:8000/movies/db/movies/`,
          headers: this.setToken(),
        })
        .then(()=> {
        })
        .catch(() => {
          this.$swal('error', '관리자 권한이 없습니다', 'error');
      })  
    }
  },
  created: function () {
    this.profileColor = this.getColors()
    axios({
      method: "get",
      url: 'http://127.0.0.1:8000/accounts/profile',
      headers: this.setToken()
    })
      .then((res) => {
        // console.log('유저정보', res) 문제없음
        this.userPK = res.data.id
        this.username = res.data.username
        this.nickname = res.data.nickname
        this.MBTI = res.data.mbti
        if (res.data.username === 'admin') {
          this.isAdmin = true
        } else {
          this.isAdmin = false 
          //  여기 is.Admin이라고 적어놨었삼 ,,
        }
        // axios({
        //   method: "post",
        //   url: 'http://127.0.0.1:8000/movies/mylists/',
        //   headers: this.setToken(),
        //   // data: this.sendData,
        //   data: {
        //     'user_id': this.userPK,
        //   },
        // })
        axios({
          method: "get",
          url: `http://127.0.0.1:8000/movies/mylists/${this.userPK}`,
          headers: this.setToken(),
        })
        .then(res => {
          // console.log('내영화', res) // 😟CLEAR !!
          let tempLists = res.data
          tempLists = _.uniqBy(tempLists, "movie")
          this.myLists = tempLists
          this.myListsTotal = tempLists.length
        })
        axios({
          method: "get",
          url:`http://127.0.0.1:8000/accounts/reviewed/${this.userPK}/`,
          headers: this.setToken()
          })
          .then(res => {
            // console.log('내리뷰', res) // 🥺내가 쓴 리뷰 가져오는건 잘 되는것 같음
              console.log(res.data)
              this.myReviewsTotal = res.data.length
              this.myReviews = res.data.slice(0, 5)
            })
      })
      .catch(()=>{
        console.log('프로필에서 난 에러')
      })

  },
  mounted: {
    
  }
}
</script>

<style scoped>
  #Profile {
    margin: 0 auto;
    margin-top: 200px;
  }
  #Profile::after {
    position: absolute;
    content: "";
    background-image: url('../../assets/star_background.png');
    width: 1920px;
    min-height: 1700px;
    height: 100%;
    top: 0;
    left: 0;
    display: block;
    z-index: -1;
    filter: blur(4px);
    opacity: .4 !important;
  }
  .cardProfile {
    margin: 0 auto;
    display: block;
    width: 100%;
    max-width: 1400px;
    /* border: 1px solid green; */
    padding: 0 20px
  }
  .cardProfile::after {
    display: block;
    content: "";
    clear: both;
  }
  
  .profileContainer {
    /* border: 1px solid red; */
    float: left;
    margin-bottom: 60px;
  }

  .profile {
    position: relative;
    width: 200px;
    height: 200px;
    margin: 20px 50px 20px 15%;
    background-color: #f08080;
    border-radius: 100px;
    overflow: hidden;
    float: left;
    margin-left: 120px;
  }
  .profile-text {
    float: left;
    /* border: 1px solid black; */
  }
  .profile img {
    position: absolute;
    width: 90%;
    height: 90%;
    top: 20px;
    left: 10px;
  }
  .nickname {
    display: block;
    float: left;
    width: 60%;
    min-height: 200px;
    border: 1px solid rgba(0,0,0,.125);
    background-color: rgba(218, 218, 218, 0.125);
    
    text-align: left;
    padding: 20px;
    margin-left: 60px;
    margin-top: 30px;
    border-radius: 6px;
  }
  /* .nickname span{
    font-weight: 700;
    font-size: 20px;
  }
  .nickname p{
    font-size: 16px;
  } */

 /* 영화리스트 */
  .mb-3 {
    margin: 0 auto;
    width: 100%;
    max-width: 1400px;
    margin-top: 10px;
  }
  .mb-3 h3 {
    width: 88%;
    /* border: 1px solid red; */
    float: left;
    margin-bottom: 0;
    padding-left: 20px;
    font-size: 28px;
  }
  .mb-3>span {
    margin: 0 auto;
    display: block;
    width: 100%;
    max-width: 1400px;
    float: left;
    font-weight: 700;
    font-size: 25px;
    /* border: 1px solid black; */
  }
  .mb-3 .b-button {
    float: right;
  }
  .mb-3::after {
    display: block;
    content: "";
    clear: both;
  }

/* 영화리스트 토글 전 */
  .allMyLists {
    float: left;
    display: inline-block;
    min-width: 1400px;
    border: 1px solid magenta;
    /* padding: 0 30px; */
  }
  .allMyLists div {
   margin: 20px 10px; 
   float: left;
  }
  .myMovieList {
    display: block;
    margin: 0 auto;
    /* border: 1px solid lime; */
    float: left;
    overflow: hidden;
    padding: 0 38px;
  }
  .deactive {
    max-height: 340px;
  }
  .myMoviePoster {
    margin: 0 auto;
    /* border: 1px solid seagreen; */
    float: left;
  }
  .myMoviePoster .posterContainer {
    display: block;
    width: 200px;
    height: 300px;
    float: left;
    margin: 20px 10px;
  }
  .posterContainer img {
    border-radius: 4px;
    width: 100%;
    height: 100%;
    transition: all 0.2s ease-in;
  }
  .myMoviePoster img:hover {
    transform: scale(1.1);
    box-shadow: 0 0 5px 0px rgba(0, 0, 0, 0.2);
  }

  .myMoviePoster1{
    position: relative;
    display: inline-block;
    border-radius: 4px;
    transition: all 0.2s ease-in;
    float: left;
    margin: 0 auto;
  }

  .myMoviePoster1 img{
    width: 200px;
    height: 300px;
    border-radius: 4px;
    transition: all 0.2s ease-in;
  }

  .myMoviePoster1:hover{
    transform: scale(1.1);
  }
/* 영화리스트 토글 후*/
  .myMoviePoster2 {
    position: relative;
    display: inline-block;
    border-radius: 4px;
    transition: all 0.2s ease-in;
    float: left;
  }
  .myMoviePoster2 img {
    width: 200px;
    height: 300px;
    border-radius: 4px;
    transition: all 0.2s ease-in;
  }

  .myMoviePoster2 img:hover {
    transform: scale(1.1);
  }

  .allMyLists::after {
    display: block;
    content: "";
    clear: both;
  }
  
  /* 리뷰 */
  #my-review{  
    position: relative;
    margin: 0 auto;
    max-width: 1400px;
    margin-top: 70px;
  } 

  #my-review h3 {
    font-weight: 700;
    text-align: left;
    padding-left: 20px;
    margin-bottom: 30px;
    font-size: 28px;
  }

  .writed-reviews {  
    display: flex;
    margin: 0 auto;
    width: 100%;
    height: 80px;
    max-width: 1474px;
    border: 1px solid rgba(0,0,0,.125);
    line-height: 80px;
    border-radius: 10px;
    margin-bottom: 20px;
    text-align: left;
    transition: all .4s;
    cursor: pointer;
  }
   .writed-reviews:hover {
    background-color: rgba(0,0,0,.125);
    box-shadow: 0 0 5px 0px rgba(0, 0, 0, 0.2);
   }
   
  /*  정렬이안돼!왜! */
 .my-review-movie {
    font-size: 15px;
    flex: 1;
    text-align: left;
    margin-left: 80px;
    /* font-weight: 700; */
    color: gray;
  }

  .my-review-title {
    font-size: 18px;
    flex: 1;
    text-align: left;
    font-weight: 600;
  }
  .my-review-content {
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    font-size: 16px;
    flex: 2;
    text-align: left;
  }
   .my-review-updated {
    font-size: 16px;
    flex: 1;
    text-align: right;
    margin-right: 30px;
    color: silver;
  }

</style>