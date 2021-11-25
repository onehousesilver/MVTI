<template>
  <div id="MyMainListItemGuest">      
    <h3>기대되는 영화를 추천해드려요♨</h3>
    <div class="upcom">
      <div v-for="latest in upcoming" :key="latest.title">
      <img :src="`https://image.tmdb.org/t/p/w200/${latest.poster_path}`"  @click="$router.push({ name: 'MovieDetail', params: { moviepk: latest.id }})" style="width:200px; cursor:pointer;">
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'MyMainListItemGuest',
  data: function () {
    return {
      upcoming: null,
    }
  },
  methods: {
    getUpcoming: function () {
      axios({
        method: 'get',
        url: 'https://api.themoviedb.org/3/movie/upcoming/',
        params: {
          api_key: 'd398b98375f1cf45b81c4980e8e1c362',
          language: 'ko-KR',
        }
      })
      .then((res) => {
        this.upcoming = res.data.results
        this.upcoming = this.upcoming.slice(0, 7)
      })
      .catch(err => {
        console.log(err)
        console.log('또 오류냐 ㅆㅃ')
      })
    },
  },
  created: function () {
    this.getUpcoming()
  }
}
</script>

<style scoped>
  #MyMainListItemGuest {
    padding-top: 80px;
  }

  #MyMainListItemGuest h3{
    margin: 0 auto;
    max-width: 1474px;
    font-weight: 700;
    margin-bottom: 20px;
    text-align: left;
    /* background-color: yellow; */
  }
  .upcom {
    margin: 0 auto;
    width: 100%;
    max-width: 1474px;
    /* border: 1px solid red; */
  }
  .upcom div {
    display: inline-block;
    width: 200px;
    height: 300px;
    /* border: 1px solid black; */
    margin: 10px 6px;
    float: left;
    transition: all .2s;
  }
  .upcom div:first-child {
    margin-left: 0;
  }
  .upcom div:last-child {
    margin-right: 0;
  }
  .upcom div:hover {
    transform: scale(1.05);
  }

  .upcom img {
    width: 100%;
    height: 100%;
    border-radius: 4px;
    box-shadow: 0 0 5px 2px rgba(0, 0, 0, 0.1);
  }
  #MyMainListItemGuest::after {
    display: block;
    content: "";
    clear: both;
  }
</style>