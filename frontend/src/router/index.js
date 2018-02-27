import Vue from 'vue'
import Router from 'vue-router'
import BuurtList from '@/components/BuurtList'
import BuurtFactsheet from '@/components/BuurtFactsheet'

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
      component: BuurtList
    },
    {
      path: '/factsheet/:buurt',
      name: 'Refactor',
      component: BuurtFactsheet
    },
    {
      path: '/factsheet',
      redirect: 'refactor/A08d'
    }
  ]
})
