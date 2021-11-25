<template>
  <div id="RecentReview">
    <h3>최신 리뷰</h3>
    <div v-if="reviews" class="recentReviewContainer">
      <div class="recentReviewForm" v-for="review in reviews" :key=review.id @click="detailFromReview(review.movie)">
        <span class="recentReviewRank">{{ rank[review.rank-1] }}</span> | 
        <span class="recentReviewTitle">{{ review.title }}</span>
        <span class="recentReviewContent">{{ review.user.nickname }} ({{ review.user.mbti }})</span>
      <!-- <span class="recentReviewTime">{{ review.user.updated_at }}</span> -->
      </div>
    </div>
    <h3 v-else>아직 작성된 리뷰가 없어요🥺</h3>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'RecentReview',
  data: function () {
    return {
        reviews: [],
        rank: ['⭐', '⭐⭐', '⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐']
    }
  },
  methods: {
    getReviews: function () {
      axios({
      method: "get",
      url: `http://127.0.0.1:8000/movies/allreviews/`,
      })
      .then((res) => {
        this.reviews = res.data.splice(0, 6)
      })
      .catch(()=>{
        console.log('리뷰리스트못가져옴;;')
      }) 
    },
    detailFromReview: function (moviePK) {
      this.$router.push({ name: 'MovieDetail', params: { moviepk: moviePK }})
    }
  },
  created: function () {
    this.getReviews()
  },
}
</script>

<style scoped>
  #RecentReview {
    margin-top: 100px;
  }
  #RecentReview h3 {
    margin: 0 auto;
    max-width: 1474px;
    font-weight: 700;
    text-align: left;
  }
  .recentReviewContainer {
    margin: 0 auto;
    padding-top: 20px;
  }
  .recentReviewForm {
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
  .recentReviewForm:hover {
    background-color: rgba(0,0,0,.125);
    box-shadow: 0 0 5px 0px rgba(0, 0, 0, 0.2);
  }

  .recentReviewRank {
    /* background-color: yellowgreen; */
    font-size: 26px;
    flex: 1;
    text-align: left;
    margin-left: 80px;
  }
  .recentReviewTitle {
    /* background-color: thistle; */
    font-size: 22px;
    font-weight: 700;
    flex: 3;
    text-align: left;
    margin-left: 60px;
  }
  .recentReviewContent {
    /* background-color: lightsteelblue; */
    font-size: 16px;
    flex: 1;
    text-align: left;
  }
</style>