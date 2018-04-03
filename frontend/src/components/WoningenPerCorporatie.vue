<template>
  <div v-if="corporaties">
    <div class="tableHeader">Aantal en spreiding woningen per aanwezige Woningcorporatie</div>

    <table class="table table-hover table-responsive" v-if="Object.keys(corporaties).length">
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
  data () {
    return {
      corporaties: null
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
    ])
  },
  methods: {
    async setBuurtData () {
      const buurtData = await privatedatasets.getBagBrk(this.buurten, this.buurt)
      this.corporaties = buurtData.data.corporaties
    }
  }
}
</script>

<style scoped>
</style>
