import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    buurt: '',
    buurten: []
  },
  actions: {
    // can be async
    setBuurt: async (context, buurt) => {
      console.log('Setting buurt to:', buurt)
      context.commit('buurt', buurt)
    },
    setBuurten: async (context, buurten) => {
      context.commit('buurten', buurten)
    }
  },
  mutations: {
    // must be synchronous
    buurt: (state, buurt) => { state.buurt = buurt },
    buurten: (state, buurten) => { state.buurten = buurten }
  },
  getters: {
    buurt: state => state.text,
    buurten: state => state.buurten
  }
})
