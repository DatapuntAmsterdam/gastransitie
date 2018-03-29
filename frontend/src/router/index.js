import Vue from 'vue'
import Router from 'vue-router'
import BuurtList from '@/components/pages/BuurtList'
import BuurtFactsheet from '@/components/pages/BuurtFactsheet'

Vue.use(Router)

export default new Router({
  // mode: 'history', // we should use this, but more server settings are needed
  base: process.env.ROUTER_BASE,
  scrollBehavior (to, from, savedPosition) {
    return { x: 0, y: 0 }
  },
  routes: [
    {
      path: '/',
      redirect: '/buurten'
    },
    {
      path: '/buurten',
      name: 'Buurten',
      component: BuurtList
    },
    {
      path: '/factsheet/:buurt',
      name: 'Buurt Factsheet',
      component: BuurtFactsheet
    },
    {
      path: '/access_token=:access_token',
      redirect: '/buurten'
    }
  ]
})
