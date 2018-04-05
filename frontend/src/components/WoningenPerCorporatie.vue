<template>
  <div>
    <div class="tableHeader">Top 5 groot eigenaars verblijfsobjecten</div>
    <piechart :buurtData="buurtData"></piechart>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import _ from 'lodash'

import privatedatasets from '../services/privatedatasets'
import Piechart from './Piechart'

export default {
  data () {
    return {
      corporaties: null,
      grootBezitters: null,
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
    ]),
    orderedGrootBezitters: function () {
      let tmp = _.filter(this.grootBezitters, item => item.statutaire_naam)
      return _.orderBy(tmp, 'thecounts', ['desc'])
    }
  },
  methods: {
    async setBuurtData () {
      this.buurtData = await privatedatasets.getBagBrk(this.buurten, this.buurt)
      this.grootBezitters = _.cloneDeep(this.buurtData.data.groot_bezitters)
    }
  }
}
</script>

<style scoped>
</style>
