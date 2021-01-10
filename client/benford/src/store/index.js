import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios";
import VueAxios from "vue-axios";

Vue.use(Vuex)
Vue.use(VueAxios, axios);

Vue.axios.defaults.baseURL = process.env.NODE_ENV === 'development' 
  ? "http://localhost:8000/api"  
  : "/api";

export default new Vuex.Store({
  state: {
    uploadResult: {
      status: null,
      data: null,
      error: null
    }
  },
  mutations: {
    UPLOAD_START(state) {
      state.status = "UPLOADING";
      state.data = null;
      state.error = null;
    },
    UPLOAD_RESULT(state, data) {
      state.status = "SUCCESS";
      state.data = data;
      state.error = null;
    },
    UPLOAD_ERROR(state, error) {
      state.status = "ERROR";
      state.data = null;
      state.error = error;
    }
  },
  actions: {
    upload({ commit }, file) {
      commit('UPLOAD_START')
      let formData = new FormData();
      formData.append('file', file);
      Vue.axios.post('upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then(result => {
        commit('UPLOAD_RESULT', result.data)
      }).catch(error => {
        commit('UPLOAD_ERROR', error);
      })
    }
  },
  modules: {
  }
})
