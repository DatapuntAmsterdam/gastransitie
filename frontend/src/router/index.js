import Vue from 'vue'
import Router from 'vue-router'
import FactsheetPage from '@/components/FactsheetPage'
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
      path: '/factsheet/:buurt',
      name: 'Factsheet',
      component: FactsheetPage
    },
    {
      path: '/buurten',
      name: 'Buurten',
      component: NeighborhoodList
    },
    {
      path: '/refactor/:buurt',
      name: 'Refactor',
      component: Refactor
    },
    {
      path: '/refactor',
      redirect: 'refactor/A08d'
    }
  ]
})
