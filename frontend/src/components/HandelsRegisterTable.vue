<template>
  <div v-if="hrData">
    <div class="tableHeader">Gevestigde bedrijven naar hoofdfunctie</div>

    <!--<td>Inschijvingen / Vestigingen:</td>-->
    <!--<td>{{hrData.data.inschrijvingen}}</td>-->

    <table class="table table-hover">
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
      </tbody>
    </table>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import privatedatasets from '../services/privatedatasets'

import _ from 'lodash'

export default {
  props: [
    'buurt'
  ],
  data () {
    return {
      hrData: null,
      q1: null,
      q1Sum: null
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
        const resultset = await privatedatasets.getJsonByName('handelsregisterbuurt', buurtId.landelijk)
        this.hrData = resultset[0]
        let q1 = this.hrData.data.q1
        this.q1 = Object.entries(q1).map(([k, v]) => ({'key': k, 'value': v}))
        this.q1Sum = Object.keys(q1).reduce((tot, key) => q1[key] + tot, 0)
      }
    }
  }
}
</script>

<style scoped>
</style>
