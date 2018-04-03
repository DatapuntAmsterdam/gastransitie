<template>
  <div v-if="buurtData">

    <div class="tableHeader">Aantal woningen naar eigendom</div>

    <table class="table table-hover table-responsive">
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
  data () {
    return {
      buurtData: null
    }
  },
  created () {
    this.setBuurtData()
  },
  computed: {
    ...mapGetters([
      'buurt',
      'buurten'
    ])
  },
  watch: {
    'buurt': function () {
      this.setBuurtData()
    }
  },
  methods: {
    async setBuurtData (buurt) {
      this.buurtData = await privatedatasets.getBagBrk(this.buurten, this.buurt)
    }
  }
}
</script>
