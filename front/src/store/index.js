import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate";
import router from '../router'
import images from './modules/images'
import workers from './modules/workers'
import axios from "axios"

Vue.use(Vuex)

export default new Vuex.Store({
  plugins: [createPersistedState({
    storage: window.sessionStorage,
  })],
  state: {
    mturk_id: null,
    server_url: 'http://3.34.46.125:8000',
    image_order: 0,
    annot_status: new Array(20).fill({'status': true})
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
    }
  },
  actions: {
    getStatus({commit}){
      const self=this;
      axios.get(self.$state.server_url + "/api/get-status",{
        params:{
            mturk_id: self.$state.mturk_id,
            doctype: self.$route.params.docType
          }
        }).then(function(res){
          console.log(res.data.status);
          commit('UPDATE_STATUS', res.data.status);
          })    
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
  },
  modules: {
    images,
    workers,
  }
})
