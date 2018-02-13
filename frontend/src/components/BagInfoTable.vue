<template>
  <div v-if="buurtData">
    <h3>Factsheet {{buurtData.naam}}</h3>

    <table style="width:100%">
      <tbody>
        <tr>
          <td style="width:50%">Naam wijk:</td>
          <td style="width:50%">{{buurtData.buurtcombinatie.naam}}</td>
        </tr>
        <tr>
          <td style="width:50%">Naam stadsdeel:</td>
          <td style="width:50%">{{buurtData.stadsdeel.naam}}</td>
        </tr>
        <tr>
          <td style="width:50%">Buurtcode:</td>
          <td style="width:50%">{{buurt}}</td>
        </tr>
      </tbody>
    </table>

    <h4>Sociaal</h4>

    <table style="width:100%">
      <tbody>
        <tr>
          <td style="width:50%">Aantal inwoners:</td>
          <td style="width:50%">tbd</td>
        </tr>
      </tbody>
    </table>

  </div>
</template>

<script>
import util from '../services/util'
import { mapGetters } from 'vuex'

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
      if (!this.buurten.length) {
        // this function can only be called meaningfully when the buurten are in the store
        console.error('buurten is not available from the Vuex store')
      } else {
        let tmp = this.buurten.find(
          d => d.vollcode === buurt
        )
        const url = 'https://api.data.amsterdam.nl/gebieden/buurt/' + tmp.landelijk
        this.buurtData = await util.readData(url)
      }
    }
  },
  watch: {
    'buurtData' (to, from) {
      if (to) {
        console.log('to', to)
        // now render our template somehow -> (name of neighborhood etc)
      }
    }
  }
}
</script>

<style scoped>
</style>
