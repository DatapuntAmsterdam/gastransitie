import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    buurt: null,
    buurten: null,
    token: null
  },
  actions: {
    // can be async
    setBuurt: async (context, buurt) => {
      context.commit('buurt', buurt)
    },
    setBuurten: async (context, buurten) => {
      context.commit('buurten', buurten)
    },
    setToken: async (context, token) => {
      context.commit('token', token)
    }
  },
  mutations: {
    // must be synchronous
    buurt: (state, buurt) => { state.buurt = buurt },
    buurten: (state, buurten) => { state.buurten = buurten },
    token: (state, token) => { state.token = token }
  },
  getters: {
    buurt: state => state.text,
    buurten: state => state.buurten,
    token: state => state.token
  }
})
