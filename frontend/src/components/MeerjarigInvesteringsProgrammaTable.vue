<template>
  <div v-if="geojson">
    <div class="tableHeader">Geplande werkzaamheden Meerjarig Investeringsplan</div>

    <table class="table table-hover">
      <tbody>
        <tr>
          <th>Datum</th>
          <th>Organisatie</th>
          <th>Opdrachtgever</th>
          <th>Nummer</th>
          <th>Omschrijving</th>
        </tr>
        <tr v-for="item in mipData" :key="item.nummmer">
          <td > {{item.datum}} </td>
          <td > {{item.organisatie}} </td>
          <td > {{item.opdrachtgever}} </td>
          <td > {{item.nummer}} </td>
          <td > {{item.omschrijving}} </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
// import util from '../services/util'
import { mapGetters } from 'vuex'
import datasets from '@/services/privatedatasets'

import _ from 'lodash'

export default {
  props: [
    'buurt'
  ],
  data () {
    return {
      geojson: null,
      mipData: null
    }
  },

  async mounted () {
    this.geojson = await datasets.getJsonByName('mip', this.buurt)
    this.mipData = this.orderedMIP()
  },
  created () {
    this.setBuurtData(this.buurt)
  },
  computed: {
    ...mapGetters([
      'buurten'
    ])
  },
  methods: {
    async setBuurtData (buurt) {
      if (!this.buurten.length) {
        // this function can only be called meaningfully when the buurten are in the store
        console.error('buurten is not available from the Vuex store')
      }
    },
    orderedMIP: function () {
      let featuredata = this.geojson.features.map(mip => mip.properties)
      // filter duplicates
      let uniqueFeatures = _.uniqBy(featuredata, 'datum')
      return _.orderBy(uniqueFeatures, 'datum', ['desc'])
    }
  }
}
</script>

<style scoped>
</style>
