<template>
  <div v-if="hrData">
    <h3>Handelsregister informatie voor {{hrData.buurt_naam}}</h3>

    <table style="width:100%">
      <tbody>
        <tr>
          <td style="width:50%">Activiteiten:</td>
          <td style="width:50%">{{hrData.data.activiteiten}}</td>
        </tr>
        <tr>
          <td style="width:50%">Inschijvingen / Vestigingen:</td>
          <td style="width:50%">{{hrData.data.inschrijvingen}}</td>
        </tr>
        <tr>
          <td style="width:50%"></td>
          <td style="width:50%"></td>
        </tr>
        <tr v-for="item in orderedHR" :key="item.key">
          <td style="width:50%"> {{item.key}} </td>
          <td style="width:50%"> {{item.value}} </td>
        </tr>

      </tbody>
    </table>
  </div>
</template>

<script>
import util from '../services/util'
import { mapGetters } from 'vuex'

import _ from 'lodash'

export default {
  props: [
    'buurt'
  ],
  data () {
    return {
      hrData: null,
      q1: null
    }
  },
  created () {
    this.setBuurtData(this.buurt)
  },
  computed: {
    ...mapGetters([
      'buurten'
    ]),
    orderedHR: function () {
      // console.log(this.q1)
      return _.orderBy(this.q1, 'value', ['desc'])
    }

  },
  methods: {
    async setBuurtData (buurt) {
      if (!this.buurten.length) {
        // this function can only be called meaningfully when the buurten are in the store
        console.error('buurten is not available from the Vuex store')
      } else {
        let buurtId = this.buurten.find(
          d => d.vollcode === buurt
        )
        const url = 'http://127.0.0.1:8000/gastransitie/api/handelsregisterbuurt/?buurt_id=' + buurtId.landelijk
        let resultset = await util.readData(url)
        this.hrData = resultset.results[0]
        let q1 = this.hrData.data.q1
        this.q1 = Object.entries(q1).map(([k, v]) => ({'key': k, 'value': v}))
      }
    }
  }
}
</script>

<style scoped>
</style>
