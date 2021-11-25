<template>
  <div id="login">
    <div class="loginForm">
      <h1>Login</h1>
      <div>
        <!-- <label for="username">E-mail </label> -->
        <input 
          type="email" 
          id="username"
          v-model="credentials.username"
          placeholder="Email"
        >
      </div>
      <div>
        <!-- <label for="password">비밀번호 </label> -->
        <input
          type="password" 
          id="password"
          placeholder="Password"
          v-model="credentials.password"
          @keyup.enter="login"
        >
      </div>
      <button @click="login">로그인</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  data: function () {
    return {
      credentials: {
        username: null,
        password: null,
      },
      imageUrl: '@/assets/background.png',
    }
  },
  methods: {
    login: function () {
      // console.log(this.credentials)
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/accounts/api-token-auth/',
        data: this.credentials,
      })
        .then(res => {
          localStorage.setItem('jwt', res.data.token)
          this.$store.dispatch('sendUserInfo', this.credentials.username)
          this.$emit('login')
          this.$router.push({ name: 'MyMain' }) // 로그인 후 이동하는 곳
        })
        .catch(() => {
          this.$swal('error', '이메일과 비밀번호를 확인 해 주세요', 'error');
          console.log('ㅄ같은로그인')
        })
    }
  }
}
</script>
<style scoped>
  #login {
    position: relative;
    margin-top: 100px;
    width: 1920px;
    height: 940px;
    /* background-image: url('../../assets/background.png');
    background-repeat: no-repeat;
    background-size: cover; */
  }
  #login::after {
    content: "";
    width: 1920px;
    height: 940px;
    display: block;
    z-index: -1;
    position: absolute;
    top: 0;
    left: 0;
    background-image: url('../../assets/background.png');
    background-repeat: no-repeat;
    background-size: cover;
    opacity: .4 !important;
  }

  .loginForm {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #f1f1f1;
    width: 480px;
    /* height: 320px; */
    border-radius: 10px;
    padding: 58px;
    padding-bottom: 30px;
    box-shadow: 0 0 8px 0px rgba(0, 0, 0, 0.1);
  }

  .loginForm h1 {
    font-size: 45px;
    font-weight: 700;
    margin-bottom: 40px;
  }

  input {
    background: transparent;
    border: 0px;
    border-bottom: 1px solid black;
    margin-bottom: 20px;
  }

  label {
    margin-right: -60px;
    line-height: 27px;
  }

  button {
    margin: 20px 0px;
    background: #494949;
    border: 0;
    color: white;
    width: 310px;
    height: 58px;
    border-radius: 6px;
    margin-top: 50px;
  }
  button:hover {
    background-color: black;
  }
</style>