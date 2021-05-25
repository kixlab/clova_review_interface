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
    server_url: 'http://3.34.46.125:8000',
    image_order: 0,
    annot_status: new Array(20).fill(false) 
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
    },
    set_step (state, step){
      state.step = step
    },
    update_status(state, status){
      state.annot_status=status
    },
    update_a_status(state, payload){
      state.annot_status[payload.idx]=payload.val
    }
  },
  getters: {
    image_url: state => {
      var docType= router.currentRoute.params.docType
      var image_order=state.image_order
 //     var imgNo=router.currentRoute.params.imgNo
      var two_digit_id = ("0" + image_order).slice(-2);
      return state.server_url + '/media/'+docType+'/'+docType+'_000' + two_digit_id + '.png'
    },
    json_url: state => {
      var docType= router.currentRoute.params.docType
      var image_order=state.image_order
//      var imgNo=router.currentRoute.params.imgNo
      var two_digit_id = ("0" + image_order).slice(-2);
      return state.server_url + '/media/'+docType+'/'+docType+'_000' + two_digit_id + '.json'
    },
    image_no: state =>{
      return state.image_order
    },
    status: state=>{
      return state.annot_status
    }
  },
  actions:{
    setStatus({commit}, status){
      console.log('setStatus called with', status)
      commit('update_status', status)
    },
    setAStatus({commit}, payload){
      console.log('setAStatus called with', payload)
      commit('update_a_status', payload)
    }
  },
  modules: {
    images,
    workers,
  }
})
