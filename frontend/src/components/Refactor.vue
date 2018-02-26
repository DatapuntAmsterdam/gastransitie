<template>
  <div>
    <oauth></oauth>
    <refactor-map :config="afwcMapConfig" :buurt="buurt"></refactor-map>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import OAuth from './OAuth'

import datasets from '@/services/privatedatasets'
import RefactorMap from './RefactorMap'
import afwcMapConfig from '../../static/afwc-map-config'

export default {
  data () {
    return {
      buurt: this.$route.params.buurt,
      afwcMapConfig
    }
  },
  components: {
    'refactor-map': RefactorMap,
    'oauth': OAuth
  },
  async mounted () {
    // remove (data is cached globally in services, just request when needed)
    let afwcGeojson = await datasets.getAfwc(this.buurt)
    let mipGeojson = await datasets.getMip(this.buurt)
    let renovatieGeojson = await datasets.getRenovatie(this.buurt)

    let energielabelGeojson = await datasets.getGeojsonByName('energielabel', this.buurt)

    console.log(
      'De data',
      afwcGeojson,
      mipGeojson,
      renovatieGeojson,
      energielabelGeojson
    )
  },
  methods: {
    ...mapActions({
      setBuurt: 'setBuurt'
    })
  },
  watch: {
    '$route' (to, from) {
      this.buurt = to.params.buurt
      this.setText()
    }
  }
}
</script>

<style scoped>
</style>
