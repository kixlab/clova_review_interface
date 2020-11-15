import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from '@/plugins/vuetify' // path to vuetify export
import global from './plugins/global';

Vue.config.productionTip = false
Vue.prototype.$localmode = false

new Vue({
  router,
  store,
  vuetify,
  global,
  render: h => h(App)
}).$mount('#app')
