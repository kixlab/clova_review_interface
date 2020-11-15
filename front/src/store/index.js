import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate";

import images from './modules/images'
import workers from './modules/workers'

Vue.use(Vuex)

export default new Vuex.Store({
  plugins: [createPersistedState({
    storage: window.sessionStorage,
  })],
  state: {
    mturk_id: null,
    server_url: 'http://localhost:8000',
    image_order: 0
  },
  mutations: {
    set_image_count (state, cnt) {
      state.image_order = cnt;
    },
    update_image_count (state) {
      state.image_order++;
    },
    set_mturk_id (state, id){
      state.mturk_id = id
    }
  },
  actions: {
  },
  getters: {
    image_url: state => {
      var two_digit_id = ("0" + state.image_order).slice(-2);
      return state.server_url + '/media/receipt_000' + two_digit_id + '.png'
    },
    json_url: state => {
      var two_digit_id = ("0" + state.image_order).slice(-2);
      return state.server_url + '/media/receipt_000' + two_digit_id + '.json'
    }
  },
  modules: {
    images,
    workers,
  }
})
