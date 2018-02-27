<template>
  <div class="container-fluid">
    <oauth></oauth>
    <div class="row">
      <div class="col-6"><bag-info-table v-if="buurten.length" :buurt="buurt"></bag-info-table></div>
      <div class="col-6"><refactor-map :config="buurtMapConfig" :buurt="buurt"></refactor-map></div>
    </div>
    <bbga-info-table v-if="buurten.length" :buurt="buurt"></bbga-info-table>
    <div class="row">
      <div class="mt-2 col-12"><h3>Corporatie bezit</h3></div>
      <div class="col-6"></div>
      <div class="col-6"><refactor-map :config="afwcMapConfig" :buurt="buurt"></refactor-map></div>
    </div>

    <div class="row" v-if="buurten.length">
      <div class="mt-2 col-12"><h3>Meerjaren Investerings Programma</h3></div>
      <div class="col-6"></div>
      <div class="col-6"><refactor-map :config="mipMapConfig" :buurt="buurt"></refactor-map></div>
    </div>

  </div>

</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import OAuth from './OAuth'

import RefactorMap from './RefactorMap'
import afwcMapConfig from '../../static/afwc-map-config'
import mipMapConfig from '../../static/mip-map-config'
import buurtMapConfig from '../../static/buurt-map-config'

import BagInfoTable from './BagInfoTable'
import BBGAInfoTable from './BBGAInfoTable.vue'

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
    'refactor-map': RefactorMap,
    'bag-info-table': BagInfoTable,
    'bbga-info-table': BBGAInfoTable,
    'oauth': OAuth
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
