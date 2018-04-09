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

/**
 * The list of panos is a list 'borrowed' from the GGW dashboard
 */
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
        // Find the pano for the current buurt with a fallback to the wijk of the buurt
        const pano = panos.find(p => p.gwb === this.buurt || // buurt
          p.gwb === this.buurt.substr(0, 3)) // wijk
        const panoUrl = pano && pano.pano
        // get the sbi (pano id) and sbh (heading) out of the url
        let sbi, sbh
        try {
          sbi = panoUrl.match(/&sbi=([^&]*)/)[1]
          sbh = panoUrl.match(/&sbh=([^&]*)/)[1]
          // The heading is a base62 encoded angle that has to be deencoded
          sbh = Math.round(base62DecodeAngle(sbh, 1))

          // Construct the url for the pano
          const width = 250
          url = `https://api.data.amsterdam.nl/panorama/thumbnail/${sbi}/?width=${width}&heading=${sbh}`
        } catch (error) {
          // On any error, url is null which is handled in the template
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
