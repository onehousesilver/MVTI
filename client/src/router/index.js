import Vue from 'vue'
import VueRouter from 'vue-router'
import Signup from '@/views/accounts/Signup'
import Login from '@/views/accounts/Login'
import MyMain from '@/views/Main/MyMain'
import SearchResult from '@/views/Main/SearchResult'
import MovieLists from '@/views/MovieList/MovieLists'
import MovieDetail from '@/views/MovieDetail/MovieDetail'
import Profile from '@/views/accounts/Profile'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'MyMain',
    component: MyMain,
  },
  {
    path: '/movielists',
    name: 'MovieLists',
    component: MovieLists,
  },
  {
    path: '/moviedetail/:moviepk',
    name: 'MovieDetail',
    component: MovieDetail,
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
  },
  {
    path: '/accounts/signup',
    name: 'Signup',
    component: Signup,
  },
  {
    path: '/accounts/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/search',
    // path: '/search/:input',
    name: 'SearchResult',
    component: SearchResult,
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
