<template>
  <div>
    <div class="tableHeader">Groot bezitters woningen</div>

    <table class="table table-hover table-responsive" v-if="orderedGrootBezitters.length">
      <thead>
        <tr>
          <th>Eigenaar</th>
          <th>Aantal woningen</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in orderedGrootBezitters" :key="item.statutaire_naam">
          <td>
            {{item.statutaire_naam}}
          </td>
          <td>
            {{item.thecounts}}
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>
      Geen gegevens beschikbaar:
    </p>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import _ from 'lodash'

import privatedatasets from '../services/privatedatasets'

export default {
  data () {
    return {
      corporaties: null,
      grootBezitters: null
    }
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
      const buurtData = await privatedatasets.getBagBrk(this.buurten, this.buurt)
      this.grootBezitters = buurtData.data.groot_bezitters
    }
  }
}
</script>

<style scoped>
</style>
