import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios";
import VueAxios from "vue-axios";

Vue.use(Vuex)
Vue.use(VueAxios, axios);

Vue.axios.defaults.baseURL = process.env.VUE_APP_MODE === 'development' 
  ? "http://localhost:8000/api"  
  : "/api";

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
  }
})
