<template>
  <div>
    <div class="tableHeader">Sociale kenmerken</div>

    <table class="table table-hover" v-if="BBGAData">
      <tbody>
        <tr>
          <td>Aantal inwoners:</td>
          <td>{{BBGAData.BEVTOTAAL || 0}}</td>
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
import { getBBGAVariables } from '../services/bbga'

const requiredVariables = [
  'BEVTOTAAL'
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
      BBGAData: null
    }
  },
  created () {
    this.setBBGAData()
  },
  methods: {
    async setBBGAData () {
      // access the relevant BBGA variable, latest year
      this.BBGAData = await getBBGAVariables(requiredVariables, -1, this.buurt)
    }
  }
}
</script>
