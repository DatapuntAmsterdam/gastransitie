import Vue from 'vue'
import Router from 'vue-router'
import BuurtList from '@/components/BuurtList'
import BuurtFactsheet from '@/components/BuurtFactsheet'

Vue.use(Router)

export default new Router({
  // mode: 'history', // we should use this, but more server settings are needed
  base: process.env.ROUTER_BASE,
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
