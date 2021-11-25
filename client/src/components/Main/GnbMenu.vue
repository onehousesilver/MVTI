<template>
  <div id="gnb" v-if="GnbShow">
    <h1>장르를 선택해 주세요</h1>
    <div v-for="(image, index) in genreImages" :key="index">
      <img :src="'http://127.0.0.1:8000'+image" alt="genre-img" style="width:100px;">
    </div>
  </div>
</template>

<script>
export default {
  name: 'GnbMenu',
  data: function () {
    return {
      GnbShow: true,
      genreImages:[
        '/media/genres/가족.jpg',
        '/media/genres/공포.jpg',
        '/media/genres/다큐.jpg',
        '/media/genres/드라마.jpg',
        '/media/genres/로맨스.jpg',
        '/media/genres/모험.jpg',
        '/media/genres/미스터리.png',
        '/media/genres/범죄.jpg',
        '/media/genres/서부.png',
        '/media/genres/스릴러.jpg',
        '/media/genres/애니메이션.png',
        '/media/genres/액션.png',
        '/media/genres/역사.jpg',
        '/media/genres/음악.png',
        '/media/genres/전쟁.jpg',
        '/media/genres/코미디.png',
        '/media/genres/판타지.png',
        '/media/genres/SF.jpg',
      ],
      genreId: {
        0: '10751', 1: '27', 2: '99', 3: '18', 4: '10749', 5: '12', 6: '9648',
        7: '80', 8: '37', 9: '53', 10: '16', 11: '28', 12: '36', 13: '10402',
        14: '10752', 15: '35', 16: '14', 17: '878', 18: '10770',
      },
    }
  }
}
</script>

<style scoped>
  #gnb {
    background: #252A36;
  }
</style>