<template>
  <div v-if="buurtData">

    <div class="tableHeader">Aantal woningen naar eigendom</div>

    <table class="table table-hover">
      <tbody>
      <tr>
        <th>Eigenaar bewoner</th>
        <th>Overig</th>
        <th>Totaal</th>
      </tr>
      <tr>
        <td>{{buurtData.data.bewoners_count}}</td>
        <td>{{buurtData.data.vbo_count - buurtData.data.bewoners_count}}</td>
        <td>{{buurtData.data.vbo_count}}</td>
      </tr>
      </tbody>
    </table>
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
      buurtData: null
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
      if (this.buurten.length) {
        const buurtDetail = this.buurten.find(b => b.vollcode === buurt)
        this.buurtData = await privatedatasets.getBagBrk(buurtDetail.landelijk)
        this.buurtData = this.buurtData[0]
      }
    }
  }
}
</script>

<style scoped>
</style>
