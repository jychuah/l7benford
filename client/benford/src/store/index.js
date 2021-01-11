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
    upload: {
      status: null,
      error: null
    },
    files: {
    },
    selected: null,
    error: null,
    loading: true
  },
  mutations: {
    UPLOAD_START(state) {
      state.upload = {
        status: "UPLOADING",
        error: null
      }
      state.selected = null 
    },
    UPLOAD_SUCCESS(state, { filename, metadata }) {
      state.upload = {
        status: "SUCCESS",
        error: null
      }
      state.files[filename] = metadata;
    },
    UPLOAD_ERROR(state, error) {
      state.upload = {
        status: "ERROR",
        error
      }
    },
    REPARSE_START(state) {
      state.histogram = {
        ...state.histogram,
        loading: true,
        error: null
      }
    },
    REPARSE_SUCCESS(state, { filename, metadata }) {
      state.files[filename] = metadata;
    },
    REPARSE_FAIL(state, error) {
      state.selected = null,
      state.error = error
    },
    LOAD_START(state) {
      state.loading = true;
      state.error = null;
    },
    LOAD_SUCCESS(state, files) {
      state.files = files;
      state.error = null;
      state.loading = false;
    },
    LOAD_ERROR(state, error) {
      state.files = {};
      state.error = error;
      state.loading = false;
    },
    SELECT(state, { filename, field }) {
      state.selected = {
        filename,
        field,
        ...state.files[filename],
      }
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
        let filename = file.name;
        let metadata = result.data;
        let field = Object.keys(metadata.histogram)[0];
        commit('UPLOAD_SUCCESS', { filename, metadata });
        commit('SELECT', { filename, field })
      }).catch(error => {
        commit('UPLOAD_ERROR', error);
      });
    },
    reparse({ commit }, { $event, filename }) {
      const delimiter = $event.target.value;
      commit('REPARSE_START')
      Vue.axios.post('reparse/', { filename, delimiter }).then(result => {
        commit('REPARSE_SUCCESS', { filename, metadata: result.data });
        commit('SELECT', { filename, field: Object.keys(result.data.histogram)[0] })
      }).catch(error => {
        commit('REPARSE_FAIL', error);
      });
    },
    load({ commit }) {
      commit('LOAD_START')
      Vue.axios.get('files').then(result => {
        commit('LOAD_SUCCESS', result.data);
        commit('SELECT', { filename: 'census_2009b', field: '7_2009' })
      }).catch(error => {
        commit('LOAD_ERROR', error);
      });
    },
    selectField({ commit, state }, $event) {
      commit('SELECT', { filename: state.selected.filename, field: $event.target.value })
    },
    selectFile({ commit, state }, { $event, file }) {
      $event.preventDefault();
      commit('SELECT', { filename: file, field: Object.keys(state.files[file].histogram)[0] })
    }
  },
  modules: {
  }
})
