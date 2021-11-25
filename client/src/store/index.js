import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex)

export default new Vuex.Store({
  plugins: [createPersistedState()],
  state: {
    CurrentUserInfo: null,
    searchKeyword: '',
    searchResults: [],
  },
  mutations: {
    SEND_KEYWORD: function (state, keyword) {
      state.searchKeyword = keyword
    },
    SEND_RESULT: function (state, result) {
      state.searchResults = []
      state.searchResults.push(result)
    },
    SEND_USER_INFO: function (state, userInfo) {
      state.CurrentUserInfo = userInfo
    }
  },
  actions: {
    sendSearchKeyword: function (context, keyword) {
      context.commit('SEND_KEYWORD', keyword)
    },
    sendResult: function(context, result) {
      context.commit('SEND_RESULT', result)
    },
    sendUserInfo: function(context, userInfo) {
      context.commit('SEND_USER_INFO', userInfo)
    }
  },
  modules: {
  }
})
