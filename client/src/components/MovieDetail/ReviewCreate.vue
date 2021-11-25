<template>
  <div id="ReviewCreate">
     <b-card bg-variant="light" class="review-form">
      <span style="font-size:16px;">이 영화에 대한 리뷰를 남겨주세요!</span>
      <div>
      <div class="star-rating" style="float:left; margin-left: 44px; margin-bottom: 12px;">
        <input type="radio" id="5-stars" name="rating" value="5" v-model="ratings" />
        <label for="5-stars" class="star pr-4">⭐</label>
        <input type="radio" id="4-stars" name="rating" value="4" v-model="ratings" />
        <label for="4-stars" class="star">⭐</label>
        <input type="radio" id="3-stars" name="rating" value="3" v-model="ratings" />
        <label for="3-stars" class="star">⭐</label>
        <input type="radio" id="2-stars" name="rating" value="2" v-model="ratings" />
        <label for="2-stars" class="star">⭐</label>
        <input type="radio" id="1-star" name="rating" value="1" v-model="ratings" />
        <label for="1-star" class="star">⭐</label>
      </div>
        <b-form-input
          id="textarea-no-resize"
          placeholder="제목을 입력해주세요."
          rows="1"
          no-resize
          v-model="sendData.title"
          style="margin: 0px 0px 10px 0px;"
        >
        </b-form-input>
      </div>
      
      <div>
        <b-form-textarea
          id="textarea-no-resize"
          placeholder="내용을 입력해주세요."
          rows="4"
          no-resize
          v-model="sendData.content"
          style="margin: 0px 0px 10px 0px"
        >
        </b-form-textarea>
        <b-button variant="outline-secondary" @click="createReview" style="float: right; ">작성완료</b-button>
      </div>
  </b-card>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ReviewCreate',
  data: function () {
    return {
        moviePk : this.$route.params.moviepk,
        reviewTitle: '',
        reviewContent: '',
        isLogin:false,
        sendData: {
          title: null,
          content: null,
          rank: 0,
        },
      ratings: null,
    }
  },
  props: {
      movieInfo: Object,
  },
  methods:{
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`
      }
      return config
    },
    who: function () {
      console.log(this.userEmail)
    },
    createReview: function () {
      this.sendData.rank = this.ratings
      axios({
        method: 'post',
        url: `http://127.0.0.1:8000/movies/review/${this.movieInfo.id}/`,
        data: this.sendData,
        headers: this.setToken(),
      })      
      .then(() => {
        // console.log(res)
        this.$emit('review-updated')

        // input 초기화
        this.sendData.title = ''
        this.sendData.content = ''
        this.ratings = null
      })
      .catch(() => {
        this.$swal('error', '로그인 후 이용해주세요', 'error');
      })
    },
  
  },

}
</script>

<style scoped>
.star-rating {
  margin: 0px 0px 0px 10px;
  display:flex;
  flex-direction: row-reverse;
  font-size:1.5em;
  justify-content:space-around;
  padding:0 .2em;
  text-align:center;
  width:5em;
}

.star-rating input {
  display:none;
}

.star-rating label {
  cursor:pointer;
  filter: grayscale(100%);
}

.star-rating :checked ~ label {
  filter: grayscale(0);
}

.star-rating label:hover,
.star-rating label:hover ~ label {
  filter: grayscale(0);
}

.review-form {
  text-align: left;
  margin: 40px auto;
  width: 100%;
  max-width: 1200px;
}

</style>