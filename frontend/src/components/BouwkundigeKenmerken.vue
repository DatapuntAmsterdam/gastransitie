<template>
  <div>
    <div class="tableHeader">Bouwjaar woningen</div>

    <table class="table table-hover table-responsive" v-if="bouwjaar && count">
      <tbody>
        <tr>
          <th v-for="g in Object.keys(bouwjaar)" :key="g">{{g}}</th>
          <th>Totaal</th>
        </tr>
        <tr>
          <td v-for="g in Object.keys(bouwjaar)" :key="g">{{bouwjaar[g]}}</td>
          <td class="text-center"><strong>{{count}}</strong></td>
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
      bouwjaar: null,
      count: 0
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

      const verdeling = buurtData.data.bouwjaar_verdeling
      let bouwjaren = Object.keys(verdeling)
        .map(key => {
          const [, from, to] = key.match(/^([-]?\d+)-(\d+)$/)
          return {from, to, count: verdeling[key]}
        })
        .sort((bj1, bj2) => bj1.from - bj2.from)

      // Convert results to std categories

      // First category starts at first non-zero time interval
      const firstNonZero = bouwjaren.findIndex(bj => bj.count > 0 && bj.to > 1920)
      const firstYear = firstNonZero === -1 ? bouwjaren[0].to : bouwjaren[firstNonZero].from
      // Last category starts at current decennium
      const year = (new Date()).getFullYear()
      const lastYear = year - (year % 10)

      // Compose object
      this.bouwjaar = {
        [`voor ${firstYear}`]: bouwjaren.slice(0, firstNonZero).reduce((sum, bj) => sum + bj.count, 0)
      }
      bouwjaren.filter(bj => firstYear <= bj.from && bj.from < lastYear)
        .forEach(bj => {
          this.bouwjaar[`${bj.from}-${bj.to}`] = bj.count
        })
      this.bouwjaar[`na ${lastYear}`] = bouwjaren
        .filter(bj => bj.from >= lastYear)
        .reduce((total, bj) => total + bj.count, 0)

      this.count = bouwjaren.reduce((total, bj) => total + bj.count, 0)
    }
  }
}
</script>

<style scoped>
</style>
