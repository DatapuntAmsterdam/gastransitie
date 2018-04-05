<template>
  <div>
    <div class="tableHeader">Top 5 groot eigenaars verblijfsobjecten (bron Kadaster)</div>
    <piechart :buurtData="buurtData"></piechart>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

import privatedatasets from '../services/privatedatasets'
import Piechart from './Piechart'

export default {
  data () {
    return {
      buurtData: null
    }
  },
  components: {
    Piechart
  },
  created () {
    this.setBuurtData()
  },
  watch: {
    'buurt': function () {
      this.setBuurtData()
    }
  },
  computed: {
    ...mapGetters([
      'buurten',
      'buurt'
    ])
  },
  methods: {
    async setBuurtData () {
      this.buurtData = await privatedatasets.getBagBrk(this.buurten, this.buurt)
    }
  }
}
</script>

<style scoped>
</style>
