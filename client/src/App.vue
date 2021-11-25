<template>
  <div id="app">
    <div id="nav">
      <span class="navBg"></span>
      <span class="navBs"></span>
      <span class="logo" @click="$router.push({ name: 'MyMain'})" style="cursor: pointer;">
        <span id="M">M</span>
        <span id="V">V</span>
        <span id="T">T</span>
        <span id="I">I</span>
      </span>
      <span class="navBar">
        <router-link :to="{ name: 'MyMain' }">Home</router-link>
        <router-link :to="{ name: 'MovieLists' }">Movies</router-link>
        <!-- <span v-if="isLogin"> -->
          <!-- <router-link :to="{ name: 'Profile' }">Profile</router-link> -->
        <router-link v-if="isLogin" @click.native="logout" :to="{ name: 'Login' }">Logout</router-link>
        <!-- </span> -->
        <!-- <span v-else> -->
        <router-link v-if="!isLogin" :to="{ name: 'Signup' }">Signup</router-link>
        <router-link v-if="!isLogin" :to="{ name: 'Login' }">Login</router-link>
        <!-- </span> -->
      </span>
      <router-link v-if="isLogin" :to="{ name: 'Profile' }"><div class="profileBtn">
        <img src="@/assets/profile_default.png" alt="">
      </div></router-link>
      <the-search-bar class="searchBar" @input-change="onInputChange"></the-search-bar>
    </div>
    <router-view @login="isLogin=true" />
  </div>
</template>

<script>
import TheSearchBar from './components/Main/TheSearchBar.vue'

export default {
  name: 'App',
  components: {
    TheSearchBar,
  },
  data: function () {
    return {
      isLogin: false,
      inputValue: null,
    }
  },
  methods: {
    onInputChange: function (inputText) {
      this.inputValue = inputText
    },
    logout: function () {
      this.isLogin = false
      localStorage.removeItem('jwt')
      this.$router.push({ name: 'MyMain' })
    }
  },
  created: function () {
    const token = localStorage.getItem('jwt')

    if (token) {
      this.isLogin = true
    }
  },
  mounted () {
    // Nav Transition🌱
    const as = document.querySelectorAll('a');
    const navBg = document.querySelector('.navBg');
    const searchBar = document.querySelector('.searchBar');
    searchBar.addEventListener('mouseover', function () {
      navBg.classList.add('atvBg')
    })
    searchBar.addEventListener('mouseout', function () {
      navBg.classList.remove('atvBg')
    })
    as.forEach((a)=>{
      a.addEventListener('mouseover', function () {
        navBg.classList.add('atvBg')
      })
      a.addEventListener('mouseout', function () {
        navBg.classList.remove('atvBg')
      })
    })

  }
}
</script>

<style>
body {
  overflow: overlay;
  overflow-x: hidden;
}
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  background-color: transparent;
}
::-webkit-scrollbar-thumb {
  border-radius: 3px;
  background-color: black;
}
::-webkit-scrollbar-button {
  width: 0;
  height: 0;
}

.logo {
  display: absolute;
  font-size: 1.5em;
  font-family: 'Soopafresh', sans-serif;     
  float: left; 
  margin-left: 30px;
  background: rgb(233, 0, 0); 
  padding: 0 12px;
  z-index: 10;
}
.logo #M {
  color: tomato;
  color: white;
}

.logo #V {
  color: lightskyblue;
  color: white;
}

.logo #T {
  color: rgb(0, 129, 39);
  color: white;
}

.logo #I {
  color: rgb(255, 201, 22);
  color: white;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  position: fixed;
  top: 0;
  z-index: 10;
  width: 100%;
  padding: 10px 0;
  /* border: 1px solid red; */
  /* background: rgba(0, 0, 0, 0.6); */
  background: transparent;
}

.navBg {
  position: absolute;
  width: 100%;
  height: 65px;
  max-height: 0px;
  top: 0;
  left: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
  transition: all .3s;
  z-index: -1;
}
.navBs {
  position: absolute;
  width: 100%;
  height: 0;
  top: 0;
  left: 0;
  box-shadow: 0 0 80px 10px rgba(0, 0, 0, 0.4);
  z-index: -1;
}

.atvBg {
  max-height: 65px;
}

#nav a {
  color: rgba(255, 255, 255, 0.6);
  /* color: #2c3e50; */
  text-decoration: none;
}

#nav a:hover {
  color: rgba(255, 255, 255, 1);
}

#nav a.router-link-exact-active {
  color: rgba(255, 255, 255, 0.8);
}

.navBar {
  display: flex;
  position: absolute;
  width: 40%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.navBar a {
  flex: 1;
  justify-content: space-between;
}

.profileBtn {
  position: relative;
  float: right;
  width: 40px;
  height: 40px;
  background-color: #494949;
  border-radius: 30px;
  overflow: hidden;
  margin-right: 1%;
}
/* 방향은 상우하좌 */
.profileBtn img {
  position: absolute;
  width: 80%;
  height: 80%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -40%);
  filter: grayscale(100%);
}
</style>