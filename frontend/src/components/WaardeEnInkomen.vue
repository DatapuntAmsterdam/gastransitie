<template>
  <div>
  <div class="tableHeader">WOZ en inkomen</div>

  <table class="table table-hover table-responsive" v-if="BBGAData">
    <tbody>
    <tr v-for="v in Object.keys(variables)" :key="v">
      <td>{{variables[v]}}</td>
      <td v-if="BBGAData[v]">&euro; {{BBGAData[v] | amount}}</td>
      <td v-else>Geen gegevens</td>
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

const variables = {
  'WWOZ_GEM': 'Gemiddelde WOZ Waarde woningen',
  'WWOZ_M2': 'Gemiddelde WOZ Waarde per m2',
  'IHHINK_GEM': 'Gemiddeld besteedbaar inkomen per huishouden'
}

export default {
  name: 'waarde-en-inkomen',
  computed: {
    ...mapGetters([
      'buurt'
    ])
  },
  watch: {
    'buurt': function () {
      this.setBBGAData()
    }
  },
  data () {
    return {
      variables,
      BBGAData: null
    }
  },
  created () {
    this.setBBGAData()
  },
  methods: {
    async setBBGAData () {
      // access the relevant BBGA variable, latest year
      this.BBGAData = await getBBGAVariables(Object.keys(variables), -1, this.buurt)
    }
  }
}
</script>
