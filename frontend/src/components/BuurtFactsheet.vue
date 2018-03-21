<template>
  <div class="container-fluid">
    <oauth></oauth>
    <div class="row">
      <div class="col-6"><bag-info-table v-if="buurten.length" :buurt="buurt"></bag-info-table></div>
      <div class="col-6"><amsterdam-map :config="buurtMapConfig" :buurt="buurt"></amsterdam-map></div>
    </div>
    <div class="row">
      <div class="mt-2 col-12"><h3>Corporatie bezit</h3></div>
      <div class="col-6"></div>
      <div class="col-6"><amsterdam-map :config="afwcMapConfig" :buurt="buurt"></amsterdam-map></div>
    </div>
    <div class="row" v-if="buurten.length">
      <div class="mt-2 col-12"><h3>Meerjaren Investerings Programma</h3></div>
      <div class="col-6"><amsterdam-mip-table v-if="buurten.length" :buurt="buurt"></amsterdam-mip-table></div>
      <div class="col-6"><amsterdam-map :config="mipMapConfig" :buurt="buurt"></amsterdam-map></div>
    </div>
    <bbga-info-table v-if="buurten.length" :buurt="buurt"></bbga-info-table>
    <div class="row">
      <div class="col-6"><bag-brk-table v-if="buurten.length" :buurt="buurt"></bag-brk-table></div>
      <div class="col-6"><handelsregister-info-table v-if="buurten.length" :buurt="buurt"></handelsregister-info-table></div>
    </div>
    <renovatie-table :buurt="buurt"></renovatie-table>
  </div>

</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import OAuth from './OAuth'

import AmsterdamMap from './AmsterdamMap'
import afwcMapConfig from '../../static/afwc-map-config'
import mipMapConfig from '../../static/mip-map-config'
import buurtMapConfig from '../../static/buurt-map-config'

import BagInfoTable from './BagInfoTable'
import BagBrkTable from './BagBrkTable'
import BBGAInfoTable from './BBGAInfoTable.vue'
import renovatieTable from './RenovatieTable.vue'

import HandelsRegisterTable from './HandelsRegisterTable.vue'
import MeerjarigInvesteringsProgrammaTable from './MeerjarigInvesteringsProgrammaTable.vue'

export default {
  data () {
    return {
      buurt: this.$route.params.buurt,
      afwcMapConfig,
      mipMapConfig,
      buurtMapConfig
    }
  },
  components: {
    'amsterdam-map': AmsterdamMap,
    'bag-info-table': BagInfoTable,
    'bag-brk-table': BagBrkTable,
    'bbga-info-table': BBGAInfoTable,
    'handelsregister-info-table': HandelsRegisterTable,
    'amsterdam-mip-table': MeerjarigInvesteringsProgrammaTable,
    'oauth': OAuth,
    'renovatie-table': renovatieTable
  },
  methods: {
    ...mapActions({
      setBuurt: 'setBuurt'
    })
  },
  computed: {
    ...mapGetters([
      'buurten'
    ])
  },
  watch: {
    '$route' (to, from) {
      this.buurt = to.params.buurt
    }
  }
}
</script>

<style scoped>
</style>
