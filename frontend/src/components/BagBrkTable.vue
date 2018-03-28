<template>
  <div v-if="buurtData">

    <h3>Kadaster Facts voor {{buurtData.naam}}</h3>

    <table class="table table-hover">
      <tbody>
        <tr>
          <td>Verblijfsobjecten:</td>
          <td>{{buurtData.data.vbo_count}}</td>
        </tr>
        <tr>
          <td>Bewoners en Eigenaar:</td>
          <td>{{buurtData.data.bewoners_count}}</td>
        </tr>
      </tbody>
    </table>

    <h3>Gebruik {{buurtData.naam}}</h3>

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
      </tbody>
    </table>

    <h3>Corporatie Tellingen {{buurtData.naam}}</h3>

    <table class="table table-hover">
      <tbody>
        <tr>
          <th>Corporatie</th>
          <th>Aantal</th>
        </tr>
        <tr v-for="item in orderedCorporatie" :key="item.key">
          <td> {{item.key}} </td>
          <td> {{item.count}} </td>
        </tr>
      </tbody>
    </table>

    <h3>Bouwkundige samenstelling {{buurtData.naam}}</h3>

    <table class="table table-hover">
      <tbody>
        <tr>
          <th>Grootte</th>
          <th>Aantal</th>
        </tr>
        <tr v-for="item in groote" :key="item.groote">
          <td> {{item.groote}} </td>
          <td> {{item.count}} </td>
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
  props: [
    'buurt'
  ],
  data () {
    return {
      buurtData: null,
      gebruik: null,
      groote: null
    }
  },
  created () {
    this.setBuurtData(this.buurt)
  },
  computed: {
    ...mapGetters([
      'buurten'
    ]),
    orderedGebruik: function () {
      return _.orderBy(this.gebruik, 'count', ['desc'])
    },
    orderedCorporatie: function () {
      return _.orderBy(this.corporaties, 'count', ['desc'])
    }

  },
  methods: {
    async setBuurtData (buurt) {
      if (!this.buurten.length) {
        // this function can only be called meaningfully when the buurten are in the store
        console.error('buurten is not available from the Vuex store')
      } else {
        let tmp = this.buurten.find(
          d => d.vollcode === buurt
        )

        this.buurtData = await privatedatasets.getBagBrk(tmp.landelijk)
        this.buurtData = this.buurtData[0]

        this.gebruik = this.buurtData['data']['gebruik']
        let c1 = this.buurtData['data']['corporaties']
        this.corporaties = Object.entries(c1).map(([k, v]) => ({'key': k, 'count': v}))
        let g = this.buurtData['data']['bouwkundige_groote']
        this.groote = Object.entries(g).map(([k, v]) => ({'groote': k, 'count': v}))
      }
    }
  }
}
</script>

<style scoped>
</style>
