<template>
  <div id="CommentList">
    <!-- <h5 class="commnetHeader" @click="getComments" style="cursor: pointer;">Comment ({{ commentCnt }})</h5> -->
    <h5 class="commnetHeader" @click="showComments=!showComments" style="cursor: pointer;">Comment ({{ comments.length }})</h5>
    <button class="moreComments" v-if="showComments" @click="showComments=!showComments"><b-icon icon="chevron-compact-down"></b-icon></button>
    <button class="closeComments" v-if="!showComments" @click="showComments=!showComments"><b-icon icon="chevron-compact-up"></b-icon></button><br>
    <span class="commentContainer" v-if="showComments">
      <div v-for="comment in comments" :key="comment.id">
        <span class="commentSep">
          <p class="commentWriter">{{ comment.user.nickname }}({{ comment.user.mbti }})</p>
          <p class="commentContent">{{ comment.content }}</p>
          <p class="commentTime">{{ comment.created_at| moment("from", "now") }}</p>
          <b-button variant="outline-dark" class="commentDelBtn" @click="deleteComment(comment.id)">댓글 삭제</b-button>
        </span>
      </div>
      <b-form-input style="width:90%;" @keyup.enter="createComments" type="text" v-model="sendData.content"></b-form-input>
      <b-button class="commentSubmitBtn" @click="createComments">작성</b-button>
    </span>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CommentList',
  props: {
    reviewPk: Number,
    commentCnt: Number,
  },
  data: function () {
    return {
      comments: [],
      showComments: false,
      sendData: {
        content: '',
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
    getComments: function () {
      // this.showComments = true
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/review/${this.reviewPk}/comment/`,
        headers: this.setToken(),
      })      
      .then((res) => {
          this.comments = res.data
      })
      .catch(err => {
          console.log(err)
      })
    },
    createComments: function () {
      axios({
        method: 'post',
        url: `http://127.0.0.1:8000/movies/review/${this.reviewPk}/comment/`,
        data: this.sendData,
        headers: this.setToken(),
      })      
      .then(() => {
        // console.log(res)
          this.sendData.content = ''
          this.getComments()
          this.$emit('comment-updated')
      })
      .catch(err => {
          console.log(err)
      })
    },
    deleteComment: function (commentPk) {
      axios({
        method: 'delete',
        url: `http://127.0.0.1:8000/movies/comments/${commentPk}/`,
        headers: this.setToken(),
      })      
      .then(() => {
          // console.log(res)
          this.getComments()
          this.$emit('comment-updated')
      })
      .catch(err => {
          console.log(err)
      })
    }
  },
  created: function () {
    this.getComments()
  }
}
</script>

<style scoped>
  button {
    border: 0;
    border-radius: 20px;
  }

  #CommentList {
    position: relative;
    padding: 20px;
    z-index: -1;
  }
  .commnetHeader {
    display: block;
    float: left;
    font-size: 20px;
    font-weight: 600;
    line-height: 50px;
    opacity: .6;
  }
  .moreComments {
    display: block;
    float: right;
    margin-top: 10px;
  }
  .closeComments {
    display: block;
    float: right;
    margin-top: 10px;
  }
  .commentContainer {
    display:block;
    background-color: white;
    margin-top: 30px;
    padding: 10px;
  }

  .commentSep {
    position: relative;
    margin-top: 30px;
    display: block;
    font-size: 18px;
    /* border: 1px solid green; */
  }
  .commentSep:first-child {
    margin-top: 0;
  }
  .commentSep p {
    display: block;
    float: left;
  }

  .commentWriter {
    font-size: 14px;
    font-weight: 600;
    margin-left: 20px;
    margin-top: 10px;
  }
  .commentContent {
    /* border: 1px solid red; */
    font-size: 18px;
    margin: 7px 20px 0px 20px;
  }
  .commentTime {
    font-size: 12px;
    position: absolute;
    top: 19px;
    right: 115px;
    color: rgba(0, 0, 0, .3);
  }
  .commentDelBtn {
    position: absolute;
    top: 10px;
    right: 10px;
    border-radius: 6px;
    font-size: 16px;
    padding: 6px 10px;
  }
  .commentSubmitBtn {
    position: absolute;
    width: 100px;
    right: 30px;
    bottom: 32px;
    border-radius: 10px;
  }
  .commentSep::after {
    display: block;
    content: "";
    clear: both;
  }
  /* 
  chevron-down
  chevron-compact-down
  <b-icon icon="chevron-compact-up"></b-icon>
  */
</style>