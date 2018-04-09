<template>
  <div>
    <div class="tableHeader">Woningvoorraad gebruiksoppervlakte</div>

    <table class="table table-hover table-responsive" v-if="grootte">
      <tbody>
        <tr>
          <th v-for="g in Object.keys(grootte)" :key="g">{{g}}m<sup>2</sup></th>
        </tr>
        <tr>
          <td v-for="g in Object.keys(grootte)" :key="g">{{grootte[g] | percentage}} </td>
        </tr>
      </tbody>
    </table>
    <p v-else>
      Geen gegevens beschikbaar
    </p>
  </div>

</template>

<script>
import { mapGetters } from 'vuex'

import privatedatasets from '../services/privatedatasets'

export default {
  data () {
    return {
      grootte: null
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
    ])
  },
  methods: {
    async setBuurtData () {
      const buurtData = await privatedatasets.getBagBrk(this.buurten, this.buurt)

      const grootte = buurtData.data.bouwkundige_groote

      // Convert results to std categories
      const oppervlakte = {}
      Object.keys(grootte).forEach(key => {
        // The oppervlakte category is n-m, eg 70-80.
        // Use a regexp to get the from value
        const [, from] = key.match(/^(\d+)-(\d+)$/)
        if (from < 90) {
          oppervlakte[key] = grootte[key]
        } else {
          // Collect all oppervlaktes > 90 in one category 90+
          oppervlakte['90+'] = (oppervlakte['90+'] || 0) + grootte[key]
        }
      })

      // Convert figures to percentages
      const totaal = Object.values(oppervlakte).reduce((i, t) => i + t)
      // Show each count as a percentage ot the total, eg 2 in category 60-70 and 2 in category 70-80
      // shows as 50%, 50%
      Object.keys(oppervlakte).forEach(key => { oppervlakte[key] = oppervlakte[key] / totaal })

      this.grootte = oppervlakte
    }
  }
}
</script>

<style scoped>
</style>
