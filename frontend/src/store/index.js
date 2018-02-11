import Vue from 'vue'
import Vuex from 'vuex'

import util from '../services/util'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    text: null,
    buurt: '',
    bbox: null,
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
      let bboxFeatures = await util.loadBbox(buurt)
      context.commit('bbox', bboxFeatures.features[0].geometry)
      context.commit('cityData', cityData)
    },
    setBbox (context, bbox) {
      context.commit('bbox', bbox)
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
    bbox (state, bbox) {
      state.bbox = bbox
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
    bbox: state => {
      return state.bbox
    },
    cityData: state => {
      return state.cityData
    }
  }
})
