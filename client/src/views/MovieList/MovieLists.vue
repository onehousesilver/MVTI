<template>
  <div id="movielists">
    <div id="listCard">
      <h1>전체 영화 목록</h1>
      <div class="moviePoster" v-for="movie in movies" :key="movie.title" :movie="movie" style="cursor: pointer;">
        <img class="movieListImg" :src="`https://image.tmdb.org/t/p/w300/${movie.poster_path}`" alt=""
          @click="$router.push({ name: 'MovieDetail', params: { moviepk: movie.id }})">
        <!-- <div @click="getDetail" style="background-color:grey;">{{ movie.title }}</div> -->
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'MovieLists',
  components: {},
  data: function () {
    return {
      movies: {},
      page_num: 1,
      index: 0,
      selectedMovieId: '',
      title: '',
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

    // movie 디테일
    getDetail: function (e) {
      const movieTitle = e.target.innerText
      this.movies.forEach(movie => {
        if (movieTitle === movie.title) {
          this.index = movie.id
        }
      })

      let moviePK = this.index
      this.$router.push({
        name: 'MovieDetail',
        params: {
          moviepk: moviePK
        }
      })
    },

    // 인피니트 스크롤
    infScroll: function () {
      let num = 2
      document.addEventListener('scroll', () => {
        const {
          scrollHeight,
          scrollTop,
          clientHeight
        } = document.documentElement
        if (scrollHeight - Math.round(scrollTop) === clientHeight) {
          axios({
              method: 'get',
              url: 'http://127.0.0.1:8000/movies/allmovies/',
              params: {
                page: num,
              }
            })
            .then((res) => {
              this.movies.push(...res.data)
              //  setTimeout(() => {
              //  this.movies.push(...res.data.results)
              //  },200)
            })
          num += 1
        }
      })
    },
  },
  created: function () {
    axios({
        method: "get",
        url: 'http://127.0.0.1:8000/movies/allmovies/',
        // headers: this.setToken()
      })
      .then((res) => {
        this.movies = res.data
        // console.log(this.movies)
      })
      .catch(() => {
        console.log('무비리스트에서 난 에러')
      })
    // this.getMovies()
  },
  mounted: function () {
    this.infScroll()
  }
}
</script>

<style scoped>
  #movielists {
    padding-top: 200px;
    background-image: url('../../assets/star_background.png');
    
  }
  #listCard {
    margin: 0 auto;
    max-width: 1400px;
    background: rgba(255, 255, 255, .2);
    border: 1px solid rgba(255, 255, 255, .2);
    backdrop-filter: blur(10px);
    border-radius: 10px;
  }

  #listCard h1 {
    color: black;
    padding: 80px 0 20px 60px;
    text-align: left;
    font-size: 45px;
    font-weight: 700;
  }
  .moviePoster {
    position: relative;
    display: inline-block;
    width: 200px;
    height: 300px;
    margin: 30px 10px;
    border-radius: 4px;
    box-shadow: 0 0 5px 2px rgba(0, 0, 0, 0.1);
  }
  .moviePoster img {
    width: 100%;
    height: 100%;
    border-radius: 4px;
    transition: all 0.2s ease-in;
  }

  .moviePoster img:hover {
    transform: scale(1.1);
  }
</style>