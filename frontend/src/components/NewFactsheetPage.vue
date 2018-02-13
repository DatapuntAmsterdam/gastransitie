<template>
  <div class="container-fluid">
    <oauth></oauth>
    <div class="row">
      <div class="col-6"><bag-info-table v-if="buurten.length" :buurt="buurt"></bag-info-table></div>
      <div class="col-6"><neighborhood-map :buurt="buurt"></neighborhood-map></div>
    </div>
  </div>
</template>

<script>
import NeighborhoodMap from './NeighborhoodMap'
import BagInfoTable from './BagInfoTable'
import OAuth from './OAuth'
import { mapGetters } from 'vuex'

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
    'oauth': OAuth
  }
}
</script>

<style scoped>
</style>
