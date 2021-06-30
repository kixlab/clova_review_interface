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
    doctype: null,
    server_url: 'http://13.125.191.49:8000',
    start_image_no: 0,
    image_order: 0,
    curr_image: 0,
    annnot_status: new Array(21).fill(false)
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
    set_start_image_no(state, img_no){
      state.start_image_no=img_no
    },
    set_step (state, step){
      state.step = step
    },
    set_curr_image(state, curr_image) {
      state.curr_image = curr_image
    },
    update_status(state, status){
      console.log("old",state.annot_status)
      console.log("new",status)
      state.annot_status=status
    },
    update_a_status(state, new_status){
    console.log('before', state.annot_status)
    state.annot_status = new_status
    console.log('after', state.annot_status)
    },
  },
  getters: {
    image_url: state => {
      var docType= router.currentRoute.params.docType
      var image_order=state.image_order
      
      var three_digit_id = ("00" + image_order).slice(-3);
      console.log("server_url ** ", state.server_url + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.png')
      return state.server_url + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.png'
      
    },
    json_url: state => {
      var docType= router.currentRoute.params.docType
      var image_order=state.image_order

      var three_digit_id = ("00" + image_order).slice(-3);
      console.log("json_url **", state.server_url + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.json')
      return state.server_url + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.json'
    },
    image_no: state =>{
      return state.image_order
    },
    getIfAllImagesAnnotated: function (state) {
      return state.annot_status.every(status => status === true)
    },
    get_curr_image: (state) => {
      return state.curr_image
    },
    getStatus: (state) => state.annot_status,


  },
  actions:{
    setCurrImage({commit}, newidx) {
      commit('set_curr_image', newidx)
    },
    setStatus({commit}, status){
      //console.log('setStatus called with', status)
      commit('update_status', status)
    },
    setAStatus({commit}, payload){
        var new_status = this.state.annot_status
        console.log('before payload', new_status)
        new_status[payload.idx] = payload.val
        console.log('after payload', new_status)
        commit('update_a_status', new_status)      
      },
  },
  modules: {
    images,
    workers,
  }
})
