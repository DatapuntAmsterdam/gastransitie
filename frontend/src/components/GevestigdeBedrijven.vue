<template>
  <div v-if="hrData">
    <div class="tableHeader">Gevestigde bedrijven naar hoofdfunctie</div>

    <table class="table table-hover table-responsive">
      <tbody>
      <tr>
        <th>Activiteit</th>
        <th>Aantal</th>
      </tr>
      <tr v-for="item in orderedHR" :key="item.key">
        <td> {{item.key}}</td>
        <td> {{item.value}}</td>
      </tr>
      <tr>
        <th>Totaal</th>
        <th>{{q1Sum}}</th>
      </tr>
      <tr>
        <th>Inschijvingen / Vestigingen</th>
        <th>{{hrData.data.inschrijvingen}}</th>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import privatedatasets from '../services/privatedatasets'

import _ from 'lodash'

export default {
  data () {
    return {
      hrData: null,
      q1: null,
      q1Sum: null
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
    orderedHR: function () {
      return _.orderBy(this.q1, 'value', ['desc'])
    }

  },
  methods: {
    async setBuurtData () {
      let buurtId = this.buurten.find(b => b.vollcode === this.buurt)
      const resultset = await privatedatasets.getJsonByName('handelsregisterbuurt', buurtId.landelijk)
      this.hrData = resultset[0]
      // The q1 naming originates in the underlying API which in turn is based on Centraal Bureau
      // Statistiek (CBS) Standaard Bedrijfsindelin (SBI) database. SBI uses three questions to
      // categorize companies. The report in our API is based on the answers to q1 (high level
      // categorization).
      let q1 = this.hrData.data.q1
      this.q1 = Object.entries(q1).map(([k, v]) => ({'key': k, 'value': v}))
      this.q1Sum = Object.keys(q1).reduce((tot, key) => q1[key] + tot, 0)
    }
  }
}
</script>

<style scoped>
</style>
