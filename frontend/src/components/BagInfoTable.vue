<template>
  <div v-if="buurtData">
    <table class="table table-hover">
      <tbody>
      <tr>
        <td>Naam buurt:</td>
        <td>{{buurtData.naam}}</td>
      </tr>
        <tr>
          <td>Naam wijk:</td>
          <td>{{buurtData.buurtcombinatie.naam}}</td>
        </tr>
        <tr>
          <td>Naam stadsdeel:</td>
          <td>{{buurtData.stadsdeel.naam}}</td>
        </tr>
        <tr>
          <td>Buurtcode:</td>
          <td>{{buurt}}</td>
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
  }
}
</script>

<style scoped>
</style>
