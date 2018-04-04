<template>
  <div>
    <div>
      <div v-for="i in Object.keys(items)" :key="i"
           v-if="complete || items[i].count > 0"
           class="legend-entry">
        <span :style="getBulletStyle(items[i])" class="legend-bullet">
          &#9634;
        </span>
        {{items[i].label}}
      </div>
    </div>

  </div>
</template>

<script>
import { LABELS } from '../services/mapStyle'

export default {
  name: 'style-legend',
  props: {
    'legend': String,
    'complete': {
      type: Boolean,
      default: true
    }
  },
  methods: {
    getBulletStyle (entry) {
      return {
        'background-color': entry.color,
        color: entry.color
      }
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

.legend-bullet {
  letter-spacing: 2px;
  border: 1px solid;
  margin-right: 7px;
}
</style>
