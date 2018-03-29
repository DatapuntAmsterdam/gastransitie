<template>
  <div v-if="buurtData">

    <div class="tableHeader">Gebruik panden</div>

    <table class="table table-hover">
      <tbody>
        <tr>
          <th>Gebruik</th>
          <th>Aantal</th>
        </tr>
        <tr v-for="item in orderedGebruik" :key="item.code">
          <td> {{item.omschrijving}} </td>
          <td> {{item.count}} </td>
        </tr>
        <tr>
          <th>Totaal</th>
          <th>{{gebruikSum}}</th>
        </tr>
      </tbody>
    </table>
  </div>

</template>

<script>
import { mapGetters } from 'vuex'

import _ from 'lodash'
import privatedatasets from '../services/privatedatasets'

export default {
  data () {
    return {
      buurtData: null,
      gebruik: null,
      gebruikSum: null,
      groote: null
    }
  },
  watch: {
    'buurt': () => this.setBuurtData()
  },
  created () {
    this.setBuurtData()
  },
  computed: {
    ...mapGetters([
      'buurten',
      'buurt'
    ]),
    orderedGebruik: function () {
      return _.orderBy(this.gebruik, 'count', ['desc'])
    },
    orderedCorporatie: function () {
      return _.orderBy(this.corporaties, 'count', ['desc'])
    }
  },
  methods: {
    async setBuurtData () {
      this.buurtData = await privatedatasets.getBagBrk(this.buurten, this.buurt)

      this.gebruik = this.buurtData.data.gebruik
      this.gebruikSum = this.gebruik.reduce((t, item) => item.count + t, 0)

      let c1 = this.buurtData.data.corporaties
      this.corporaties = Object.entries(c1).map(([k, v]) => ({'key': k, 'count': v}))
      let g = this.buurtData.data.bouwkundige_groote
      this.groote = Object.entries(g).map(([k, v]) => ({'groote': k, 'count': v}))
    }
  }
}
</script>
