<template>
  <div id="SearchResult">
    <h3 class="searchKeyword">'<span class="searchKeywordHighlight">{{ searchKeyword }}</span>' 검색결과</h3>
    <div>
      <div class="search">
        <div class="search-poster" v-for="result in newResults" :key="result.id">
          <b-row no-gutters class="search-block">
          <b-col md="2">
              <b-card-img class="poster-img" :src="`https://image.tmdb.org/t/p/w300/${result.poster_path}`" alt="" @click="movieDetail(result)"></b-card-img>
            </b-col>
            <b-col md="6">
              <b-card-body class="search-text">
                    <h3 class="title" @click="movieDetail(result)">{{ result.title }}</h3> <br>
                    <h5 class="original-title">{{ result.original_title }}</h5>
                <b-card-text>
                  <span>제작: {{ result.release_date }}</span>
                </b-card-text>
              </b-card-body>
            </b-col>
          </b-row>
        </div>
      </div>
    </div>

  <h3 style="font-weight: 700; margin-top: 80px;" v-if="!newResults">검색된 영화가 없습니다.</h3>

  </div>
</template>

<script>
export default {
  name: 'SearchResult',
  data: function () {
    return {
      keyword: '',
    }
  },
  methods: {
    movieDetail: function (result) {
      console.log(result)
      this.$router.push({ name: 'MovieDetail', params: { moviepk: result.id } })
    },
  },
  computed: {
    searchKeyword: function () {
      // this.keyword = this.$store.state.searchKeyword
      console.log(this.$store.state.searchKeyword)
      return this.$store.state.searchKeyword
    },
    newResults: function () {
      return this.$store.state.searchResults[0]
    } 
  }
}
</script>

<style scoped>
  #SearchResult {
    margin-top: 180px;
  }
  .searchKeyword {
    font-weight: 700;
    margin-bottom: 100px;
  }
  .searchKeywordHighlight {
    color: rgb(220, 0, 0);
  }

  .search {
    margin: 30px 15%;
  }
  .search-poster {
    padding: 30px;
    border: 1px solid rgba(0,0,0,.125);
    border-radius: 6px;
    margin-bottom: 20px
  }

  .poster-img {
    border-radius: 7px;
    width: 280px;
    height: 400px;
    cursor:pointer; 
    transition: ease-out .4s;
  }

  .poster-img:hover {
    transform: scale(1.05);
    transition: transform 0.1s;
    filter: brightness(70%);
  }

  .title {
    display: inline;
    cursor: pointer; 
    font-weight: bold;
  }

  .title:hover {
    text-decoration: underline;  
  }

  .original-title {
    display: inline;
  }

  .search-text {
    margin: 0px 0px 0px 15%;
    float: left;
    text-align: left;
  }

  .search-block{
    /* margin: 0px 0px 40px 0px; */
    margin-left: 6px;
    transition: all .4s;
  }
</style>