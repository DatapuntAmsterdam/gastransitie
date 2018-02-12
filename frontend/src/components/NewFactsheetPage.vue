<template>
  <div>
    <neighborhood-map :buurt="buurt"></neighborhood-map>
  </div>
</template>

<script>
import NeighborhoodMap from './NeighborhoodMap'

export default {
  data () {
    return {
      buurt: this.$route.params.buurt
    }
  },
  components: {
    'neighborhood-map': NeighborhoodMap
  }
}
</script>

<style scoped>
</style>
