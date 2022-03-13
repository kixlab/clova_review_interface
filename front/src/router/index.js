import Vue from 'vue'
import VueRouter from 'vue-router'
import Landing from '../views/Landing.vue'
import PageNotFound from '../views/404.vue'
import Dashboard from '../views/Dashboard.vue'
import ImageView from '../views/ImageView.vue'

//import Resolution from '../views/Annotation.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/dashboard/:docType',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/imageview/:docType',
    name: 'ImageView',
    component: ImageView
  },
  {
    path: '/landing',
    name: 'Landing',
    component: Landing,
    alias: '/'
  },
  {
    path: "*",
    name: '404',
    component: PageNotFound
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
