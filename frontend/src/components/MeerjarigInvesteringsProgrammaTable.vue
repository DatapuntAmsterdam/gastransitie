<template>
  <div v-if="geojson">
    <table class="table table-hover">
      <tbody>
        <tr>
          <th>organisatie</th>
          <th>datum</th>
          <th>nummer</th>
          <th>opdrachtgever</th>
          <th>omschrijving</th>
        </tr>
        <tr v-for="item in orderedMIP" :key="item.nummer">
          <td > {{item.organisatie}} </td>
          <td > {{item.datum}} </td>
          <td > {{item.nummer}} </td>
          <td > {{item.opdrachtgever}} </td>
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
  },
  created () {
    this.setBuurtData(this.buurt)
  },
  computed: {
    ...mapGetters([
      'buurten'
    ]),
    orderedMIP: function () {
      let featuredata = this.geojson.features.map(mip => mip.properties)
      // filter duplicates
      let uniqueFeatures = _.uniqBy(featuredata, 'datum')
      return _.orderBy(uniqueFeatures, 'datum', ['desc'])
    }
  },
  methods: {
    async setBuurtData (buurt) {
      if (!this.buurten.length) {
        // this function can only be called meaningfully when the buurten are in the store
        console.error('buurten is not available from the Vuex store')
      }
    }
  }
}
</script>

<style scoped>
</style>
