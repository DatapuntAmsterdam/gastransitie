<template>
  <div v-if="buurtData">

    <h3>Kadaster Facts voor {{buurtData.naam}}</h3>

    <table style="width:100%">
      <tbody>
        <tr>
          <td style="width:50%">Verblijfsobjecten:</td>
          <td style="width:50%">{{buurtData.data.vbo_count}}</td>
        </tr>
        <tr>
          <td style="width:50%">Bewoners en Eigenaar:</td>
          <td style="width:50%">{{buurtData.data.bewoners_count}}</td>
        </tr>
      </tbody>
    </table>

    <h3>Gebruik {{buurtData.naam}}</h3>

    <table style="width:100%">
      <tbody>
        <tr>
          <th style="width:50%">Gebruik</th>
          <th style="width:50%">Aantal</th>
        </tr>
        <tr v-for="item in orderedGebruik" :key="item.code">
          <td style="width:50%"> {{item.omschrijving}} </td>
          <td style="width:50%"> {{item.count}} </td>
        </tr>
      </tbody>
    </table>

    <h3>Corporatie Tellingen {{buurtData.naam}}</h3>

    <table style="width:100%">
      <tbody>
        <tr>
          <th style="width:50%">Corporatie</th>
          <th style="width:50%">Aantal</th>
        </tr>
        <tr v-for="item in orderedCorporatie" :key="item.key">
          <td style="width:50%"> {{item.key}} </td>
          <td style="width:50%"> {{item.count}} </td>
        </tr>
      </tbody>
    </table>

    <h3>Bouwkundige samenstelling {{buurtData.naam}}</h3>

    <table style="width:100%">
      <tbody>
        <tr>
          <th style="width:50%">Grootte</th>
          <th style="width:50%">Aantal</th>
        </tr>
        <tr v-for="item in groote" :key="item.groote">
          <td style="width:50%"> {{item.groote}} </td>
          <td style="width:50%"> {{item.count}} </td>
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
        // const url = 'https://api.data.amsterdam.nl/gebieden/buurt/' + tmp.landelijk
        const url = 'http://127.0.0.1:8000/gastransitie/api/bag/' + tmp.landelijk + '/'
        this.buurtData = await util.readData(url)
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
