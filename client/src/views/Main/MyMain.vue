<template>
  <div id="#my_main">
    <!-- swiper 캐러샐 -->
    <swiper class="swiper" :options="swiperOption">
    <swiper-slide v-for="(movie, index) in movies" :key="index" 
    class="nowPlaying" :style="{ 'background-image': 'url(https://image.tmdb.org/t/p/original/' + movie.backdrop_path + ')'}">
      <!-- <div style="color:white">{{genreResults}}</div> -->
      <div class="mainDescrip">
      <span class="genreBadge" v-for="(gen,idx) in genreResults[index]" :key="idx">
        {{ gen.name }}
      </span>
        <h2 style="font-weight: 700; text-overflow:elipsis;">{{ movie.title }}</h2>
        <p style="color: gray;">{{ movie.original_title }}</p>
        <p class="movieOverview">{{ movie.overview }}</p>
        <button class="playTrailerBtn" @click="getVideo(movie.id)">▶ Play Trailer</button>
        <button class="getDetailBtn" @click="$router.push({ name: 'MovieDetail', params: { moviepk: movie.id }})"> Details</button>
      </div>
    </swiper-slide>
    <div class="swiper-button-prev" slot="button-prev"></div>
    <div class="swiper-button-next" slot="button-next"></div>
    </swiper>

    <!-- 트레일러 모달 -->
    <div v-if="showModal" class="modalContainer">
      <div v-show="src" class="modalContent">
        <iframe width="1000" height="560" :src="src" title="YouTube video player" frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen="allowfullscreen"></iframe>
      </div>
      <h3 v-show="!src" class="noTrailer">트레일러가 없습니다</h3>
      <b-icon @click="toggleModal" icon="x" scale="5" class="modalClose"></b-icon>
      <!-- <button @click="toggleModal">닫기</button> -->
    </div>

    <!-- 추천 영화 리스트 -->
    <span v-if="isLogin">
      <my-main-list-item></my-main-list-item>
      <my-main-list-item-guest></my-main-list-item-guest>
    </span>
    <span v-else>
      <my-main-list-item-guest></my-main-list-item-guest>
    </span>
    <recent-review></recent-review>
  </div>
</template>

<script>
import axios from 'axios'
// import GnbMenu from '@/components/Main/GnbMenu.vue'
// import MyCarousel from '@/components/Main/MyCarousel.vue'

import MyMainListItem from '@/components/Main/MyMainListItem.vue'
import MyMainListItemGuest from '@/components/Main/MyMainListItemGuest.vue'
import RecentReview from '@/components/Main/RecentReview.vue'

import { Swiper, SwiperSlide } from 'vue-awesome-swiper'
import 'swiper/css/swiper.css'
// import MyCarousel from '../../components/Main/MyCarousel.vue'

// const API_KEY = process.env.VUE_APP_TMDB_API_KEY

export default {
  name: 'MyMain',
  components: {
    // GnbMenu,
    // MyCarousel,
    MyMainListItem,
    MyMainListItemGuest,
    RecentReview,
    Swiper,
    SwiperSlide,
  },
  data: function () {
  return {
    genreResults: [],
    subscribe: false,
    isLogin: false,
    inputValue: null,
    movies: null,
    moviePk: this.$route.params.moviepk,
    videoKey: null,
    showModal: false,
    src: true,
    isSrc: false,
    swiperOption: {
        scrollbar: {
          el: '.swiper-scrollbar',
          hide: true
        },
        autoplay: {
          delay: 5000,
        },
        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev'
        },
        loop: true,
      }
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
    toggleModal: function () {
      this.showModal = !this.showModal
      this.src = !this.src
    },
    getMains: function () {
      // 상영중 영화 불러오기
      axios({
        method: 'get',
        // url로 작성하기
        url: 'https://api.themoviedb.org/3/movie/now_playing',
        params: {
          api_key: 'd398b98375f1cf45b81c4980e8e1c362',
          language: 'ko-KR',
        }
      })
      .then((res) => {
        this.movies = res.data.results
        // console.log(res.data.results)
        this.getGenres(res.data.results)
      })
      .catch(() => {
        console.log('상영중 영화가 없습니다')
      })
    },
    logout: function () {
      this.isLogin = false
      localStorage.removeItem('jwt')
    },
    getVideo: function (moviePK) {
      this.src = false
      this.toggleModal()
      axios({
        method: 'get',
        url: `https://api.themoviedb.org/3/movie/${moviePK}/videos`,
        params: {
          api_key: 'd398b98375f1cf45b81c4980e8e1c362',
          language: 'ko-KR',
        },
      })
      .then(res => {
        this.src = `https://www.youtube.com/embed/${res.data.results[0].key}?autoplay=1&mute=1`;
      })
      .catch(() => this.src = false)
    },
    addMovieList: function (moviePK) {
      this.subscribe = true,
        axios({
          method: 'post',
          url: `http://127.0.0.1:8000/movies/mylists/${moviePK}/`,
          headers: this.setToken(),
        })
        .then(res => {
          console.log(res)
        })
        .catch(() => {
          this.$swal({title:'이런!',text:'영화가 아직 없어요😢  업로드를 기대해주세요.',color: 'rgba(0, 0, 0, 0.8)',position:'top-center'})
        })
    },
    removeMovieList: function (moviePK) {
      this.subscribe = false,
        axios({
          method: 'delete',
          url: `http://127.0.0.1:8000/movies/mylists/${moviePK}/`,
          headers: this.setToken(),
        })
        .then(res => {
          console.log(res)
        })
    },
    getGenres: function (movies) {
      this.genreResults = []
      movies.forEach(movie => {
        const moviePK = movie.id
        axios({
          method: 'get',
          url: `https://api.themoviedb.org/3/movie/${moviePK}`,
          params: {
            api_key: 'd398b98375f1cf45b81c4980e8e1c362',
            language: 'ko-KR',
          },
        })
        .then(res => {
          this.genreResults.push(res.data.genres)
        })
      });
    }
  },
  created: function () {
    const token = localStorage.getItem('jwt')
    if (token) {
      this.isLogin = true
      }
    // this.getMains() 
  },
  watch: {
    showModal: function() {
      if(this.showModal){
        document.documentElement.style.overflow = 'hidden'
        return
      }
      document.documentElement.style.overflow = 'auto'
    },
  },
  mounted() {
    this.getMains() 
  }
}
</script>

<style>
  #my_main {
    position: relative;
    width: 100%;
  }
  .nowPlaying {
    position: relative;
    background-repeat: no-repeat;
    background-size: 100% auto;
  }
  .swiper {
    width: 100%;
    height: 960px;
  }
  .swiper-button-prev {
    color: white;
  }
  .swiper-button-next {
    color: white;
  }

  .mainDescrip {
    position: absolute;
    width: 860px;
    height: 450px;
    top: 40%;
    left: 12%;
    padding: 40px;
    padding-bottom: 50px;
    background-color: rgba(0, 0, 0, .6);
    backdrop-filter: blur(4px);
    color: white;
    text-align: left;
    border-radius: 8px;
  }
  .mainDescrip .genreBadge {
    font-size: 16px;
    margin-right: 4px;
  }
  .mainDescrip h2 {
    text-align: left;
    margin-top: 10px;
  }
  .movieOverview {
    height: 146px;
    overflow: hidden;
    text-overflow: ellipsis;
    word-wrap: break-word;
    display: -webkit-box;
    -webkit-line-clamp: 5;
    -webkit-box-orient: vertical;
    line-height: 1.5;
  }
  .playTrailerBtn {
    background-color: rgb(233, 0, 0);
    color: white;
    border: 0;
    border-radius: 100px;
    padding: 13px 25px;
    margin-right: 20px;
    transition: all .2s;
  }
  .playTrailerBtn:hover {
    box-shadow: 0 0 16px 1px rgb(255, 32, 32);
  }
  .getDetailBtn {
    /* width: 175px; */
    background-color: rgb(37, 37, 37);
    color: white;
    border: 0;
    border-radius: 100px;
    padding: 15px 25px;
    text-align: left;
    transition: all .2s;
  }
  .getDetailBtn:hover {
    box-shadow: 0 0 16px 1px rgba(182, 182, 182, 0.507);
  }
  .noTrailer {
    color: white;
    text-align: ceter;
    line-height: 960px;
  }
  .modalContainer {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    z-index: 9999;
    backdrop-filter: blur(10px);
  }
  .modalContent {
    position: absolute;
    top: 20%;
    left: 50%;
    transform: translate(-50%);    
  }
  .modalClose {
    position: absolute;
    top: 10%;
    left: 50%;
    transform: translate(-50%, -50%);
    color:white;
    cursor:pointer;
  }
</style>