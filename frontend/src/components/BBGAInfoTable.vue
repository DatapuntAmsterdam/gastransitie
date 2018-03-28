<template>
  <div>
    <div class="row">
      <div class="col-6">
        <h3>Sociaal</h3>

        <table class="table table-hover">
          <tbody>
            <tr>
              <td>Aantal inwoners:</td>
              <td>{{BBGAData.BEVTOTAAL}}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <h4>Bevolking naar migratie achtergrond</h4>
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
              <td>{{BBGAData.BEVAUTOCH_P}} %</td>
              <td>{{BBGAData.BEVWEST_P}} %</td>
              <td>{{BBGAData.BEVSUR_P}} %</td>
              <td>{{BBGAData.BEVANTIL_P}} %</td>
              <td>{{BBGAData.BEVTURK_P}} %</td>
              <td>{{BBGAData.BEVMAROK_P}} %</td>
              <td>{{BBGAData.BEVNW_P}} %</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import util from '../services/util'
import { mapGetters } from 'vuex'

let requiredVariables = [
  'BEVTOTAAL', 'BEVSUR_P', 'BEVTURK_P', 'BEVANTIL_P', 'BEVMAROK_P', 'BEVNW_P', 'BEVWEST_P', 'BEVAUTOCH_P']

export default {
  props: [
    'buurt'
  ],
  data () {
    let placeholder = {}
    for (let variable of requiredVariables) {
      placeholder[variable] = ''
    }
    return {
      BBGAData: placeholder
    }
  },
  created () {
    this.setBBGAData(this.buurt)
  },
  computed: {
    ...mapGetters([
      'buurten'
    ])
  },
  methods: {
    setBBGAData (buurt) {
      // access the relevant BBGA variable, latest year
      this.getBBGAVariables(requiredVariables, 2017)
    },
    async getBBGAVariables (vars, year) {
      let BBGAData = {}
      for (let variabele of vars) {
        let url = `https://api.data.amsterdam.nl/bbga/cijfers/?variabele=${variabele}&gebiedcode15=${this.buurt}&jaar=${year}`
        let data = await util.readData(url)
        if (data.count !== 1) {
          console.error('We received more than one result for variable, neighborhood, year combination')
        }
        BBGAData[variabele] = data.results[0].waarde
      }
      this.BBGAData = BBGAData
    }
  }
}
</script>

<style scoped>
</style>
