<template>
  <div>
    <div class="tableHeader">Woningvoorraad gebruiksoppervlakte</div>

    <table class="table table-hover" v-if="grootte">
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
    this.setBuurtData(this.buurt)
  },
  computed: {
    ...mapGetters([
      'buurten',
      'buurt'
    ])
  },
  methods: {
    async setBuurtData (buurt) {
      const buurtData = await privatedatasets.getBagBrk(this.buurten, this.buurt)

      const grootte = buurtData.data.bouwkundige_groote

      // Convert results to std categories
      const oppervlakte = {}
      Object.keys(grootte).forEach(key => {
        const [, from] = key.match(/^(\d+)-(\d+)$/)
        if (from < 90) {
          oppervlakte[key] = grootte[key]
        } else {
          oppervlakte['90+'] = (oppervlakte['90+'] || 0) + grootte[key]
        }
      })

      // Convert figures to percentages
      const totaal = Object.values(oppervlakte).reduce((i, t) => i + t)
      Object.keys(oppervlakte).forEach(key => { oppervlakte[key] = oppervlakte[key] / totaal })

      this.grootte = oppervlakte
    }
  }
}
</script>

<style scoped>
</style>
