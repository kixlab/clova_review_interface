import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate";
import router from '../router'
import images from './modules/images'
import workers from './modules/workers'

Vue.use(Vuex)

export default new Vuex.Store({
  plugins: [createPersistedState({
    storage: window.sessionStorage,
  })],
  state: {
    mturk_id: null,
    server_url: 'http://13.209.4.171:8000',
  },
  mutations: {
    set_mturk_id (state, id){
      state.mturk_id = id
    },
    set_step (state, step){
      state.step = step
    }
  },
  actions: {
  },
  getters: {
    image_url: state => {
      var docType= router.currentRoute.params.docType
      var imgNo=router.currentRoute.params.imgNo
      var two_digit_id = ("0" + imgNo).slice(-2);
      return state.server_url + '/media/'+docType+'/'+docType+'_000' + two_digit_id + '.png'
    },
    json_url: state => {
      var docType= router.currentRoute.params.docType
      var imgNo=router.currentRoute.params.imgNo
      var two_digit_id = ("0" + imgNo).slice(-2);
      return state.server_url + '/media/'+docType+'/'+docType+'_000' + two_digit_id + '.json'
    }
  },
  modules: {
    images,
    workers,
  }
})
