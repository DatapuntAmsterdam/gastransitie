<template>
  <div>
    <div class="tableHeader">Bevolking buurt naar migratie achtergrond</div>

    <table class="table table-hover">
      <thead>
        <tr>
          <th>Nederlands</th>
          <th>Overig Westers</th>
          <th>Surinaams</th>
          <th>Antilliaans</th>
          <th>Turks</th>
          <th>Marrokaans</th>
          <th>Overig niet westers</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>{{BBGAData.BEVAUTOCH_P || 0}}%</td>
          <td>{{BBGAData.BEVWEST_P || 0}}%</td>
          <td>{{BBGAData.BEVSUR_P || 0}}%</td>
          <td>{{BBGAData.BEVANTIL_P || 0}}%</td>
          <td>{{BBGAData.BEVTURK_P || 0}}%</td>
          <td>{{BBGAData.BEVMAROK_P || 0}}%</td>
          <td>{{BBGAData.BEVNW_P || 0}}%</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { getBBGAVariables } from '../services/bbga'

const requiredVariables = [
  'BEVSUR_P', 'BEVTURK_P', 'BEVANTIL_P', 'BEVMAROK_P', 'BEVNW_P', 'BEVWEST_P', 'BEVAUTOCH_P'
]

export default {
  computed: {
    ...mapGetters([
      'buurt'
    ])
  },
  watch: {
    'buurt': () => this.setBBGAData()
  },
  data () {
    return {
      BBGAData: {}
    }
  },
  created () {
    this.setBBGAData()
  },
  methods: {
    async setBBGAData (buurt) {
      // access the relevant BBGA variable, latest year
      this.BBGAData = await getBBGAVariables(requiredVariables, -1, this.buurt)
    }
  }
}
</script>
