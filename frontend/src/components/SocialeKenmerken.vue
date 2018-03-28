<template>
  <div>
    <div class="tableHeader">Sociale kenmerken</div>

    <table class="table table-hover">
      <tbody>
        <tr>
          <td>Aantal inwoners:</td>
          <td>{{BBGAData.BEVTOTAAL || 0}}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { getBBGAVariables } from '../services/bbga'

const requiredVariables = [
  'BEVTOTAAL'
]

export default {
  props: [
    'buurt'
  ],
  data () {
    return {
      BBGAData: {}
    }
  },
  created () {
    this.setBBGAData(this.buurt)
  },
  methods: {
    async setBBGAData (buurt) {
      // access the relevant BBGA variable, latest year
      this.BBGAData = await getBBGAVariables(requiredVariables, 2017, buurt)
    }
  }
}
</script>

<style scoped>
</style>
