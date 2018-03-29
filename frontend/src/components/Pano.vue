<template>
  <div>
    <img v-if="url" :src="url">
    <p v-else>
      Geen foto beschikbaar van {{buurtData.naam}}
    </p>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

import panos from '../../static/panos'
import { base62DecodeAngle } from '../services/base62'

export default {
  data () {
    return {
      url: null
    }
  },
  computed: {
    ...mapGetters([
      'buurt',
      'buurtData'
    ])
  },
  methods: {
    /**
     * Find the most mathing pano for the current gwb
     */
    updatePano () {
      let url = null
      if (this.buurt) {
        const pano = panos.find(p => p.gwb === this.buurt || // buurt
          p.gwb === this.buurt.substr(0, 3)) // wijk
        const panoUrl = pano && pano.pano
        let sbi, sbh
        try {
          sbi = panoUrl.match(/&sbi=([^&]*)/)[1]
          sbh = panoUrl.match(/&sbh=([^&]*)/)[1]
          sbh = Math.round(base62DecodeAngle(sbh, 1))

          const width = 250
          url = `https://api.data.amsterdam.nl/panorama/thumbnail/${sbi}/?width=${width}&heading=${sbh}`
        } catch (error) {
        }
      }
      this.url = url
    }
  },
  watch: {
    'buurt' () {
      this.updatePano()
    }
  },
  created () {
    this.updatePano()
  }
}
</script>

<style scoped>
</style>
