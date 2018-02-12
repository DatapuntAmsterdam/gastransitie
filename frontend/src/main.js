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

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'leaflet/dist/leaflet.css'

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
      let buurten = this.$store.state.buurten
      if (!buurten.length) {
        const url = 'http://localhost:8000/gastransitie/api/buurt/'
        let results = await util.readProtectedPaginatedData(
          url,
          util.getGeoJSONData,
          util.getNextPage
        )
        let tmp = results.map(function (d, i) {
          return {vollcode: d.properties.vollcode, naam: d.properties.naam}
        })
        tmp.sort(function (a, b) {
          if (a.naam > b.naam) {
            return +1
          } else if (a.naam < b.naam) {
            return -1
          } else {
            return 0
          }
        })
        this.setBuurten(tmp)
      }
    }
  }
})

vueApp.init()
