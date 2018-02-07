import Vue from 'vue'
import Vuex from 'vuex'

import util from '../services/util'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    text: null,
    buurt: '',
    cityData: {}
  },
  actions: {
    // can be async
    setText (context, text) {
      context.commit('text', text)
    },
    async setBuurt (context, buurt) {
      context.commit('buurt', buurt)
      context.commit('cityData', {})
      let cityData = await util.loadCityData(buurt)
      context.commit('cityData', cityData)
    },
    setCityData (context, cityData) {
      context.commit('cityData', cityData)
    }
  },
  mutations: {
    // must be synchronous
    text (state, text) {
      state.text = text
    },
    buurt (state, buurt) {
      state.buurt = buurt
    },
    cityData (state, cityData) {
      state.cityData = cityData
    }
  },
  getters: {
    text: state => {
      return state.text
    },
    buurt: state => {
      return state.text
    },
    cityData: state => {
      return state.cityData
    }
  }
})
