import Vue from 'vue'
import VueRouter from 'vue-router'
import Annotation from '../views/Annotation.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'Annotation',
    component: Annotation
  }
]

const router = new VueRouter({
  routes
})

export default router
