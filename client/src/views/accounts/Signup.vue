<template>
  <div id="Signup">
    <div class="signupForm"> 
      <h1>Signup</h1>
    <div>
      <!-- <label for="username">E-mail </label> -->
      <input 
        type="email" 
        id="username"
        placeholder="Email"
        v-model="credentials.username"
      >
    </div>
    <div>
      <!-- <label for="password">비밀번호 </label> -->
      <input 
        type="password" 
        id="password"
        placeholder="Password"
        v-model="credentials.password"
      >
    </div>
    <div>
      <!-- <label for="passwordConfirmation">비밀번호 확인 </label> -->
      <input 
        type="password" 
        id="passwordConfirmation"
        placeholder="Password Comfirm"
        v-model="credentials.passwordConfirmation"
        @keyup.enter="signup"
      >
    </div>
    <div>
      <!-- <label for="nickname">닉네임 </label> -->
      <input 
        type="text" 
        id="nickname"
        placeholder="Nickname"
        v-model="credentials.nickname"
      >
    </div>
    <div>
      <!-- <label for="mbti">MBTI: </label> -->
      <input 
        type="text" 
        id="mbti"
        placeholder="MBTI"
        v-model="credentials.mbti"
      >
    </div>
    <button @click="isValid" @keyup.enter="isValid">회원가입</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import swal from 'sweetalert'
// import VueSweetalert2 from 'vue-sweetalert2';


export default {
  name: 'Signup',
  data: function () {
    return {
      credentials: {
        username: null,
        password: null,
        passwordConfirmation: null,
        nickname: null,
        mbti: null,
      },
    }
  },
  methods: {
    signup: function () {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/accounts/signup/',
        data: this.credentials
      })
        .then(() => {
          // console.log(res)
          this.$router.push({ name: 'Login'})
        })
        .catch(err => {
          console.log(err)
        })
    },
    isValid: function () {
      // console.log(this.credentials)
      // console.log(this.credentials.mbti.toUpperCase())
      const mbti_list = ['ISTJ','ISFJ','INFJ','INTJ','ISTP','ISFP','INFP','INTP','ESTP','ESFP','ENFP','ENTP','ESTJ','ESFJ','ENFJ','ENTJ']
      if (this.credentials.username === null || 
          this.credentials.password === null ||
          this.credentials.passwordConfirmation == null || 
          this.credentials.nickname == null || this.credentials.mbti == null) {
            swal ("필수 정보를 모두 입력해주세요.", {
              dangerMode: true,
            })
      } else {
        if (!this.credentials.username.includes('@')) {
          swal ("이메일 형식을 확인해 주세요", { dangerMode: true, })
        } else if (this.credentials.password != this.credentials.passwordConfirmation) {
          swal ("비밀번호를 확인해 주세요", { dangerMode: true, })
        } else if (this.credentials.mbti.length != 4 || mbti_list.includes(this.credentials.mbti.toUpperCase()) === false) {
          swal ("올바른 MBTI를 입력해 주세요", { dangerMode: true, })
        } else {
          this.credentials.mbti = this.credentials.mbti.toUpperCase()
          this.signup(this.credentials)
        } // else 끝    
      } // isValid else 끝    
    } // isValid 함수 끝
  }, // methods 끝
} // export default 끝
</script>
<style scoped>

  #Signup {
    position: relative;
    margin-top: 100px;
    width: 1920px;
    height: 937px;
    /* background-image: url('../../assets/background.png');
    background-repeat: no-repeat;
    background-size: cover; */
  }
  .signupForm {
    position: absolute;
    top: 50%;
    left: 55%;
    transform: translate(-50%, -50%);
    background: #f1f1f1;
    width: 480px;
    /* height: 620px; */
    border-radius: 10px;
    padding: 58px;
    box-shadow: 0 0 8px 0px rgba(0, 0, 0, 0.1);
  }
  #Signup::after {
    content: "";
    width: 1920px;
    height: 937px;
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

  .signupForm h1 {
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
