<template>
  <div>
    <card title="Algemene gegevens">
      <div class="row">
        <div class="col-lg-6 col-md-12"><bag-info-table v-if="buurten.length" :buurt="buurt"></bag-info-table></div>
        <div class="col-lg-6 col-md-12"><amsterdam-map :config="buurtMapConfig" :buurt="buurt"></amsterdam-map></div>
      </div>
      <bbga-info-table v-if="buurten.length" :buurt="buurt"></bbga-info-table>
    </card>

    <card title="Corporatie bezit">
      <div class="row">
        <div class="col-lg-6 col-md-12"></div>
        <div class="col-lg-6 col-md-12"><amsterdam-map :config="afwcMapConfig" :buurt="buurt"></amsterdam-map></div>
      </div>
    </card>

    <card title="Meerjaren Investerings Programma">
      <div class="row">
        <div class="col-12"><amsterdam-mip-table v-if="buurten.length" :buurt="buurt"></amsterdam-mip-table></div>
        <div class="col-12"><amsterdam-map :config="mipMapConfig" :buurt="buurt"></amsterdam-map></div>
      </div>
    </card>

    <card title="Kadaster">
      <div class="row">
        <div class="col-lg-6 col-md-12"><bag-brk-table v-if="buurten.length" :buurt="buurt"></bag-brk-table></div>
        <div class="col-lg-6 col-md-12"><handelsregister-info-table v-if="buurten.length" :buurt="buurt"></handelsregister-info-table></div>
      </div>
    </card>

    <card title="Renovatie">
      <renovatie-table :buurt="buurt"></renovatie-table>
    </card>

  </div>

</template>

<script>
import { mapGetters, mapActions } from 'vuex'

import card from './Card'

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
    'card': card,
    'amsterdam-map': AmsterdamMap,
    'bag-info-table': BagInfoTable,
    'bag-brk-table': BagBrkTable,
    'bbga-info-table': BBGAInfoTable,
    'handelsregister-info-table': HandelsRegisterTable,
    'amsterdam-mip-table': MeerjarigInvesteringsProgrammaTable,
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
