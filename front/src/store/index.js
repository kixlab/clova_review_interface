import Vue from 'vue'
import Vuex from 'vuex'
import images from './modules/images'
import workers from './modules/workers'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    server_url: 'http://localhost:8000',
    image_order: 0
  },
  mutations: {
    update_image_count (state) {
      state.image_order++;
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
