// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import { mapActions } from 'vuex'

import store from './store'

import 'leaflet/dist/leaflet.css'

import '../static/app.scss'

import util from './services/util'

Vue.use(VueAxios, axios)

Vue.config.productionTip = false

Vue.filter('percentage', x => String((x * 100).toFixed(2)) + '%')
Vue.filter('amount', x => `${x.toLocaleString('NL')}`)

/* eslint-disable no-new */
let vueApp = new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>',
  methods: {
    ...mapActions({
      setBuurten: 'setBuurten'
    }),
    async init () {
      // following line implicitly initalizes the neighborhood id mappings in ./services/datasets.js
      const buurten = await util.loadBuurten()
      this.setBuurten(buurten)
    }
  }
})

vueApp.init()
