<template>
  <div class="searchbar">
    <span>
      <input @keyup.enter="searchMovie" placeholder="검색어를 입력해주세요" type="text" v-model="sendData.searchInput">
      <b-icon class="searchIcon" icon="search" @click="searchMovie" style="cursor:pointer; color: white;"></b-icon>
    </span>
    <!-- <button @click="searchMovie">검색</button> -->
  </div>
</template>

<script>
import axios from'axios'
import { BIcon } from 'bootstrap-vue';

export default {
  name: 'SearchBar',
  components: { BIcon },
  data: function () {
    return {
      sendData: {
        searchInput : ''
      },
      searchResults: [],
    }
  },
  methods: {
    searchMovie: function () {
      console.log(this.sendData.searchInput)
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/search/${this.sendData.searchInput}/`,// 요렇게 url에 쿼리로 담아서 넘겨주셔야합니다
      })
      .then((res) => {
        this.searchResults = res.data
        
        this.$store.dispatch('sendSearchKeyword', this.sendData.searchInput)
        this.$store.dispatch('sendResult', this.searchResults)
        this.$router.push({ name: 'SearchResult' })
        this.sendData.searchInput = ''
      })
    },
  }
}
</script>

<style scoped>
  .searchbar {
    position: relative;
    float: right;
    margin-top: 6px;
    margin-right: 20px;
  }
  span {
    top: 0;
    right: 0;
  }
  input {
    background: transparent;
    border: 0;
    /* border-bottom: 2px solid rgba(0, 0, 0, 0.6); */
    border-bottom: 2px solid rgb(128, 128, 128);
    padding-left: 10px;
    padding-right: 60px;
    padding-bottom: 2px;
    font-size: 18px;
  }
  input:focus {
    outline: none;
    color: rgb(165, 165, 165);
  }
  .searchIcon {
    position: absolute;
    right: 0;
    top: 38%;
    transform: translate(-50%, -50%);
  }

</style>