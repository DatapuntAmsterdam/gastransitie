import Vue from 'vue'
import Router from 'vue-router'
import NeighborhoodList from '@/components/NeighborhoodList'
import Refactor from '@/components/Refactor'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      redirect: '/buurten'
    },
    {
      path: '/buurten',
      name: 'Buurten',
      component: NeighborhoodList
    },
    {
      path: '/factsheet/:buurt',
      name: 'Refactor',
      component: Refactor
    },
    {
      path: '/factsheet',
      redirect: 'refactor/A08d'
    }
  ]
})
