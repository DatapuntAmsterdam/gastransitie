import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
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
      path: '/home',
      name: 'Home',
      component: Home
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
