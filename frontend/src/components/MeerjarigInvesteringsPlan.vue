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
  data () {
    return {
      geojson: null,
      mipData: null
    }
  },
  created () {
    this.setBuurtData()
  },
  computed: {
    ...mapGetters([
      'buurt'
    ])
  },
  watch: {
    'buurt': function () {
      this.setBuurtData()
    }
  },
  methods: {
    async setBuurtData () {
      this.geojson = await datasets.getJsonByName('mip', this.buurt)
      this.mipData = this.orderedMIP()
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
