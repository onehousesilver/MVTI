<template>
  <div>
    <h3>내 영화 리스트</h3>
    <div v-for="poster in myPosters" :key="poster.id">
        <img :src="poster.reviewed" alt="" @click="movieDetail(poster)" style="cursor:pointer;">
    </div>
    <h3>내가 쓴 리뷰</h3>
    userPK : {{ userPK }}
    <button @click="getReviewedMovies">리뷰임시가져오기버튼</button>
    {{ myReviews }}
  </div>
</template>

<script>
import axios from 'axios'
import _ from 'lodash'

export default {
  name: 'MyReview',
  props: {
    userPK: Number,
  },
  data: function () {
    return {
      myReviews: null,
      myPosters: null,
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
    getReviewedMovies: function () {
    axios({
    method: "get",
    url:`http://127.0.0.1:8000/accounts/reviewed/${this.userPK}/`,
    headers: this.setToken()
    })
    .then((res) => {
        // console.log(res.data)
        this.myReviews = res.data.slice(0, 5)
        let tempPosters = res.data
        tempPosters = _.uniqBy(tempPosters, "movie")
        this.myPosters = tempPosters
    })
    },
    movieDetail: function (poster) {
      this.$router.push({ name: 'MovieDetail', params: { moviepk: poster.movie } })
    },
  },
  // created: function () {
  //   axios({
  //   method: "get",
  //   url:`http://127.0.0.1:8000/accounts/reviewed/${this.userPK}/`,
  //   headers: this.setToken()
  //   })
  //   .then((res) => {
  //       // this.reviews = res.data
  //       console.log(res.data)
  //       this.myReviews = res.data.slice(0, 5)
  //   })
  // },
//   updated: function () {
    // this.getReviewedMovies()
//   },
} 
</script>

<style>

</style>