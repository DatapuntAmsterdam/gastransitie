import Vue from 'vue'
import Router from 'vue-router'
import FactsheetPage from '@/components/FactsheetPage'
import NeighborhoodList from '@/components/NeighborhoodList'

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
    }
  ]
})
