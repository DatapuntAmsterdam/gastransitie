// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import BootstrapVue from 'bootstrap-vue'
import { mapActions } from 'vuex'

import store from './store'

// import 'bootstrap/dist/css/bootstrap.css'
// import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'leaflet/dist/leaflet.css'

import 'stijl/css/ams-stijl.css'

import util from './services/util'

Vue.use(VueAxios, axios)

Vue.use(BootstrapVue)

Vue.config.productionTip = false

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
      const buurten = await util.loadBuurten()
      this.setBuurten(buurten)
    }
  }
})

vueApp.init()
