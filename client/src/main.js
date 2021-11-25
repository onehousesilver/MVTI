import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import VueAwesomeSwiper from 'vue-awesome-swiper'
import VueMoment from 'vue-moment'
import moment from "moment";

import VueSweetalert2 from 'vue-sweetalert2'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import Vuesax from 'vuesax'
import 'vuesax/dist/vuesax.css'

// If you don't need the styles, do not connect
import 'sweetalert2/dist/sweetalert2.min.css'
import 'swiper/css/swiper.css'

Vue.use(VueSweetalert2).use(VueAwesomeSwiper).use(VueMoment, { moment }).use(BootstrapVue).use(BootstrapVueIcons).use(Vuesax);

Vue.config.productionTip = false

moment.locale("ko");
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')