import Vue from 'vue'
import VueRouter from 'vue-router'
import Landing from '../views/Landing.vue'
import InformedConsent from '../views/InformedConsent.vue'
import Instruction from '../views/Instruction.vue'
import Annotation from '../views/Annotation.vue'
import AfterDone from '../views/AfterDone.vue'
import PageNotFound from '../views/404.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/annotation',
    name: 'Annotation',
    component: Annotation
  },
  {
    path: '/landing',
    name: 'Landing',
    component: Landing,
    alias: '/'
  },
  {
    path: '/informed-consent',
    name: 'InformedConsent',
    component: InformedConsent
  },
  {
    path: '/instruction',
    name: 'Instruction',
    component: Instruction
  },
  {
    path: '/after-done',
    name: 'AfterDone',
    component: AfterDone
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
