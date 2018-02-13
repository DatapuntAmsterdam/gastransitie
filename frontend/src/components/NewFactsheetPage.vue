<template>
  <div class="container-fluid">
    <oauth></oauth>
    <div class="row">
      <div class="col-6"><bag-info-table v-if="buurten.length" :buurt="buurt"></bag-info-table></div>
      <div class="col-6"><amsterdam-map :buurt="buurt"></amsterdam-map></div>
    </div>
    <bbga-info-table v-if="buurten.length" :buurt="buurt"></bbga-info-table>
    <div class="row" v-if="buurten.length">
      <div class="mt-2 col-12"><h3>Corporatie bezit</h3></div>
      <div class="col-6"></div>
      <div class="col-6"><afwc-map :buurt="buurt"></afwc-map></div>
    </div>
    <div class="row" v-if="buurten.length">
      <div class="mt-2 col-12"><h3>Meerjarig Investerings Plan</h3></div>
      <div class="col-6"></div>
      <div class="col-6"><mip-map :buurt="buurt"></mip-map></div>
    </div>
  </div>
</template>

<script>
import NeighborhoodMap from './NeighborhoodMap'
import BagInfoTable from './BagInfoTable'
import OAuth from './OAuth'
import { mapGetters } from 'vuex'
import BBGAInfoTable from './BBGAInfoTable.vue'
import AmsterdamMap from './AmsterdamMap.vue'
import AfwcMap from './AfwcMap.vue'
import MipMap from './MipMap.vue'

export default {
  data () {
    return {
      buurt: this.$route.params.buurt
    }
  },
  computed: {
    ...mapGetters([
      'buurten'
    ])
  },
  components: {
    'neighborhood-map': NeighborhoodMap,
    'bag-info-table': BagInfoTable,
    'bbga-info-table': BBGAInfoTable,
    'amsterdam-map': AmsterdamMap,
    'afwc-map': AfwcMap,
    'mip-map': MipMap,
    'oauth': OAuth
  }
}
</script>

<style scoped>
</style>
