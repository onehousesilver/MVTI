<template>
  <div id="MovieDetail">
      <div>
      <!--영화 포스터, 내용-->
      <b-card no-body id="overflow-hidden" style="max-width: 1200px;">
        <b-row no-gutters>
          <b-col md="4" class="card-img" >
            <b-card-img :src="`https://image.tmdb.org/t/p/w300/${selectedMovieInfo.poster_path}`" alt="Image"
              class="rounded-2" ></b-card-img>
            </b-col>
            <b-col md="3" class="card-body">
            <b-card-body>
              <span v-for="genre in genres" :key="genre.id">
                <span style="margin:4px; font-size: 16px;">{{ genre.name }}</span>
              </span>
              <h1 style="font-weight: 700; margin: 0; margin-top: 6px;">{{ selectedMovieInfo.title }}</h1>
              <span style="color: gray; font-size: 18px; padding-left: 4px;">{{ selectedMovieInfo.original_title }}</span>
              <b-card-text>
                <h4 style="margin: 20px 0;">⭐ <span style="font-weight: 600;">{{ selectedMovieInfo.vote_average }}</span></h4>
                <span class="mbtiPick" v-if="pick">{{ pick }}</span>
                <span class="noPick" v-else>NO</span>
                <span> pick !</span>
                <br>
                <span class="detailOverview">{{ selectedMovieInfo.overview }} </span>
                <br>
                <b-button pill variant="outline-danger"
                v-if='!subscribe' @click="addMovieList"
                style="margin-bottom: 60px;"
                >+ add My List</b-button>
                <b-button pill variant="outline-danger" style="margin-bottom: 60px;" v-else @click="removeMovieList">- remove from List</b-button>
                &nbsp;&nbsp;
              </b-card-text>
            </b-card-body>
          </b-col>
            <!-- 영화 예고편 -->
              <div>
                <div id="area" v-if="teaser">
                  <iframe id="video" width="560" height="460" :src="`https://www.youtube.com/embed/${teaser}?mute=1`"
                    title="YouTube video player" frameborder="0"
                    allow="accelerometer; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen="allowfullscreen"
                    style="margin-top: 20px;"></iframe>
                </div> 
              </div>
              <!--배우 리스트-->
              <h4 style="text-align: left; margin: 10px 0px 20px 20px; font-weight: 700;"> 주요출연진 </h4>
                <div class="img-padding" v-for="cast in casts" :key="cast.name" style="flex:1;">
                  <b-card-img :src="`https://image.tmdb.org/t/p/w200/${cast.profile_path}`" alt="Image" style="width=50px" class="actor-img"></b-card-img>
                    <b><h5 style="margin: 5px 0px 0px 0px;">{{ cast.name }}</h5></b>
                    <div style="margin: 0px 0px 15px 0px;"><span style="color:grey;">{{ cast.character }}</span></div>
                </div>
        </b-row>
      </b-card>
    </div>
  
    <!-- 영화 배우 리스트
    <div>
      <b-card no-body class="actor-list">
          <b-row no-gutters md="4">
            <h3 style="text-align: left; margin: 10px 0px 10px 25px"> 주요출연진 </h3>
              <div class="img-padding" v-for="cast in casts" :key="cast.name" style="flex:1;">
                <b-card-img :src="`https://image.tmdb.org/t/p/w200/${cast.profile_path}`" alt="Image" style="width=50px" class="actor-img"></b-card-img>
                  
                  <b><h5 style="margin: 5px 0px 0px 0px;">{{ cast.name }}</h5></b>
                  <div style="margin: 0px 0px 15px 0px;"><span style="color:grey;">{{ cast.character }}</span></div>
              </div>
          </b-row>
      </b-card>
    </div>-->
    <div>

      <!-- 리뷰 -->
      <div class="container" style="display=block;">
        <span id="rateMe3" class="rating-faces"></span>
      </div>
      <review-create :movieInfo="selectedMovieInfo" @review-updated="getReviews"></review-create>

      <review-list :movieInfo="selectedMovieInfo" :propReviews="reviews" @review-updated="getReviews"
        :reviewCnt="selectedMovieInfo.reviews_count"></review-list>-
    </div>
</div>
</template>

<script>
import axios from 'axios'
import _ from 'lodash'

import ReviewCreate from '@/components/MovieDetail/ReviewCreate.vue'
import ReviewList from '@/components/MovieDetail/ReviewList.vue'

export default {
  name: 'MovieDetail',
  components: {
    ReviewCreate,
    ReviewList,
  },
  data: function () {
    return {
      subscribe: false,
      videoAvailable: false,
      selectedMovie: '',
      selectedMovieInfo: {},
      casts: {},
      genres: {},
      reviewReload: {},
      moviePk: this.$route.params.moviepk,
      reviews: null,
      teaser: null,
      pick: null,
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
    getReviews: function () {
      axios({
          method: "get",
          url: `http://127.0.0.1:8000/movies/review/${this.moviePk}/`,
        })
        .then((res) => {
          this.reviews = res.data
        })
        .catch((err) => {
          console.log(err)
        })
    },
    addMovieList: function () {
      this.subscribe = true,
        axios({
          method: 'post',
          url: `http://127.0.0.1:8000/movies/mylists/${this.moviePk}/`,
          headers: this.setToken(),
        })
        .then(() => {
          // console.log(res)
        })
        .catch(() => {
          this.$swal('error', '로그인 후 이용해주세요', 'error');
      })
    },
    removeMovieList: function () {
      this.subscribe = false,
        axios({
          method: 'delete',
          url: `http://127.0.0.1:8000/movies/mylists/${this.moviePk}/`,
          headers: this.setToken(),
        })
        .then(()=> {
          // console.log(res)
        })
        .catch(() => {
          this.$swal('error', '로그인 후 이용해주세요', 'error');
      })  
    },  
  },
  mounted: function () {
    const moviePK = this.$route.params.moviepk
    // 영화정보📺(DB)
    axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/allmovies/${moviePK}/`,
      })
      .then(res => {
        // MBTI pick🎀
        const reviews = res.data.reviews
        let mbtis = []
        reviews.forEach(review => {
          mbtis.push(review.user.mbti)
        });
        this.pick = _.uniq(mbtis)[0]

        // 가져온 movie data에 대한 id로 TMDB에 접근
        this.selectedMovieInfo = res.data

        // 영화 배우🦸‍♀️(TMDB)
        axios({
            method: 'get',
            url: `https://api.themoviedb.org/3/movie/${moviePK}/credits`,
            params: {
              api_key: 'd398b98375f1cf45b81c4980e8e1c362',
              language: 'ko-KR',
            },
          })
          .then(res => {
            this.casts = res.data.cast.slice(0, 5)
          })

        // 영화 장르🎫(TMDB)
        axios({
            method: 'get',
            url: `https://api.themoviedb.org/3/movie/${moviePK}`,
            params: {
              api_key: 'd398b98375f1cf45b81c4980e8e1c362',
              language: 'ko-KR',
            },
          })
          .then(res => {
            this.genres = res.data.genres
          })

        // 트레일러🎬(TMDB)
        axios({
            method: 'get',
            url: `https://api.themoviedb.org/3/movie/${moviePK}/videos`,
            params: {
              api_key: 'd398b98375f1cf45b81c4980e8e1c362',
              language: 'ko-KR',
            },
          })
          .then(res => {
            const videos = res.data.results
            const teaser = _.filter(videos, {
              site: 'YouTube',
              type: 'Teaser'
            })

            if (videos.length && teaser.length) {
              this.videoAvailable = true
              this.teaser = teaser[teaser.length - 1].key
            } else {
              this.videoAvailable = false
            }
          })

      })
      .catch(() => {
        console.log("또류 ㅅㅂ")

      })
    this.getReviews()
  }

}
</script>

<style scoped>

  #MovieDetail {
    margin-top: 100px;
  }
  #MovieDetail::after {
    position: absolute;
    content: "";
    background-image: url('../../assets/star_background.png');
    width: 1920px;
    min-height: 2000px;
    height: 100%;
    top: 0;
    left: 0;
    display: block;
    z-index: -1;
    filter: blur(4px);
    opacity: .4 !important;
  }
  .mbtiPick {
    background: #c4191D;
    color: white;
    padding: 6px 8px;
    border-radius: 8px;
  }
  .noPick {
    background: rgb(66, 66, 66);
    color: white;
    padding: 6px 8px;
    border-radius: 8px;
  }

  #overflow-hidden {
   margin: auto;
   padding: 30px 30px 0px 30px;
   top: 50%;
  }

 .card-body {
   padding: 0px 10px 10px 15px;
   text-align: left;
   width: 800px;
   
   /* width: 600px;
   height: 500px; */
 }

 .rounded-2 {
    margin: 0px 0px 0px 12px;    
 }

 .card-img {
    width: 350px;
    height: 470px;
    
 }
 #area {
    position: relative; /* absolute는 부모가 relative일 때 부모를 따라간다. */
    width: 100%;
    padding-bottom: 56.25%; /* 16:9 비율 */
    padding: 0px 0px 20px 0px;
 }

#video {
  width: 100%;
  height: 500px;
}

.actor-list {
  margin: 20px auto 20px;
  padding: 10px 30px 0px 30px;
  top: 50%;

}

.actor-img {
  width: 160px;
  height: 230px;
}

.card {
  display: inline-table;
}

.detailOverview {
  display: block;
  margin-top: 20px;
  font-size: 18px;
}
</style>