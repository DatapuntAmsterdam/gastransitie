<template>
  <div>
    <div>
      <div v-for="i in Object.keys(items)" :key="i"
           v-if="complete || items[i].count > 0"
           class="legend-entry">
        <legend-bullet :color="items[i].color"></legend-bullet>
        {{items[i].label}}
      </div>
    </div>

  </div>
</template>

<script>
import { LABELS } from '../services/mapStyle'
import LegendBullet from './LegendBullet'

export default {
  components: {LegendBullet},
  name: 'style-legend',
  props: {
    'legend': String,
    'complete': {
      type: Boolean,
      default: true
    }
  },
  data () {
    return {
      items: []
    }
  },
  created () {
    this.items = LABELS[this.legend]
  }
}
</script>

<style lang="scss" scoped>
.legend-entry {
  margin-top: .3rem;
}
</style>
