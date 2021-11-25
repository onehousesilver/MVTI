<template>
  <div id="MyMainListItem">
    <!-- <button @click="getAllMyLists">모든리스트</button> -->
    <div v-show="isResponse">
      <h3>당신과 같은 <span class="highlight">{{ MBTI }}</span>가 좋아한 영화입니다</h3>
      <div class="recommended" v-if="recommends">
        <div class="recoContents" v-for="(vote, recommend, index) in recommends"  :key="index" @click="getIdToDetail(recommend)">
        <span v-if="index < 7">
          <span class="recoBadge">{{ vote }} PICK!</span>
          <img :src="recommend" alt="recommended_poster" style="width:200px; cursor:pointer;">
        </span>
        </div>
      </div>
      <div v-if="!recommends">
        <h5 class="recommendedMessage">아직 다른{{ MBTI }}를 가진 🙋‍♀️가 좋아한 영화가 없어요😥</h5>
      </div>
    </div>
  </div>
</template>

<script scoped>
import axios from 'axios'
import _ from 'lodash'

export default {
  name: 'MyMainListItem',
  data: function () {
    return {
      MBTI: null,
      results: [],
      movies: null,
      recommends: null,
      isResponse: false,
      length: 7,
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
    getIdToDetail: function (poster_path) {
      const find_results = _.find(this.results, {'poster_path': poster_path})
      this.$router.push({ name: 'MovieDetail', params: { moviepk: find_results.movie }})
    },
    getAllMyLists: function () {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/mylists/`,
        headers: this.setToken(),
      })
      .then(res => {
        this.results = []
        let movies = res.data
        this.movies = res.data
        this.results = _.filter(movies, {'user_mbti' : this.MBTI})
      })
      .then(() => {
        let poster_path = _.countBy (this.results, "poster_path")
        this.recommends = _.fromPairs(_.sortBy(_.toPairs(poster_path), 1).reverse())
        this.isResponse = true
      })
    },
  },
  created: function () {
    axios({
      method: "get",
      url: 'http://127.0.0.1:8000/accounts/profile',
      headers: this.setToken()
    })
      .then((res) => {
        const data_mbti = res.data.mbti
        this.MBTI = data_mbti
      })
    this.getAllMyLists()   
  },
  mounted: function () {
  }
}
</script>

<style scoped>
  #MyMainListItem {
    padding-top: 80px;
  }
  #MyMainListItem h3 {
    margin: 0 auto;
    max-width: 1474px;
    font-weight: 700;
    margin-bottom: 20px;
    text-align: left;
    /* background-color: yellow; */
  }

  .recommended {
    margin: 0 auto;
    width: 100%;
    max-width: 1474px;
    max-height: 300px;
    /* border: 1px solid red; */
    float: left;
    margin-left: 50%;
    transform: translate(-50%);
    /* overflow-y: hidden; */
  }
  .recoContents {
    float: left;
    display: inline-block;
    width: 200px;
    margin: 0px 6px;
    border-radius: 4px;
    overflow: hidden;
    box-shadow: 0 0 5px 2px rgba(0, 0, 0, 0.1);
    transition: all .2s;
  }
  .recoContents:first-child {
    margin-left: 0;
  }
  .recoContents:nth-child(7) {
    margin-right: 0;
  }
  .recoContents:hover {
    transform: scale(1.05);
  }

  .recoBadge {
    position: absolute;
    background: #c4191D;
    color: white;
    padding: 5px 8px;
    border-radius: 4px;
  }

  #MyMainListItem::after {
    display: block;
    content: "";
    clear: both;
  }
</style>