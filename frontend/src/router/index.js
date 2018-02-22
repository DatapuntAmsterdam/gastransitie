import Vue from 'vue'
import Router from 'vue-router'
import NewFactsheetPage from '@/components/NewFactsheetPage'
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
      component: NewFactsheetPage
    },
    {
      path: '/buurten',
      name: 'Buurten',
      component: NeighborhoodList
    }
  ]
})
