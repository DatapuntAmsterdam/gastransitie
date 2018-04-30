<template>
  <div v-if="energieData">
    <div class="tableHeader">Energieverbruik</div>

    <table class="table table-hover table-responsive">
      <tbody>
      <tr>
        <td>Gas Aansluitingen:</td>
        <td>{{energieData.data.gas.aansluitingen}}</td>
      </tr>
        <tr>
          <td>Gas Verbruik:</td>
          <td>{{energieData.data.gas.m3}} m3</td>
        </tr>
        <tr>
          <td>Elektra aansluitingen:</td>
          <td>{{energieData.data.elk.aansluitingen}}</td>
        </tr>
        <tr>
          <td>Elektra verbruik:</td>
          <td>{{energieData.data.elk.Kwh}} Kwh</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { getDataByName } from '../services/datasets'

export default {
  data () {
    return {
      energieData: null
    }
  },
  created () {
    this.getData()
  },
  computed: {
    ...mapGetters([
      'buurt'
    ])
  },
  methods: {
    async getData () {
      if (this.buurt) {
        let data = await getDataByName('energie', this.buurt)
        this.energieData = data[0]
      }
    }
  },
  watch: {
    'buurt': function () {
      this.getData()
    }
  }
}
</script>
