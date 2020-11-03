import Vue from 'vue'
import Vuex from 'vuex'
import images from './modules/images'
import workers from './modules/workers'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    server_url: 'http://localhost:8000'
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    images,
    workers,
  }
})
