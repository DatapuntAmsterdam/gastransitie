<template>
  <div v-if="corporaties">
    <div class="tableHeader">Aantal en spreiding woningen per aanwezige Woningcorporatie</div>

    <table class="table table-hover" v-if="Object.keys(corporaties).length">
      <tbody>
        <tr>
          <th v-for="c in Object.keys(corporaties)" :key="c">
            {{c}}
          </th>
        </tr>
        <tr>
          <td v-for="c in Object.keys(corporaties)" :key="c">
            {{corporaties[c]}}
          </td>
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
  props: [
    'buurt'
  ],
  data () {
    return {
      corporaties: null
    }
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
      if (this.buurten) {
        const buurtDetail = this.buurten.find(b => b.vollcode === buurt)
        const buurtData = await privatedatasets.getBagBrk(buurtDetail.landelijk)
        this.corporaties = buurtData[0].data.corporaties
      }
    }
  }
}
</script>

<style scoped>
</style>
