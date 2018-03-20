<template>
  <div></div>
</template>

<script>
import L from 'leaflet'
import datasets from '@/services/privatedatasets'

export default {
  props: [
    'config',
    'map',
    'buurt'
  ],
  data () {
    return {
      geojson: {type: 'FeatureCollection', features: []},
      geojsonLayer: null
    }
  },
  async mounted () {
    console.assert(this.config !== null && this.config !== undefined, 'A config entry is needed to render this layer.')
    this.geojson = await datasets.getJsonByName(this.config.dataset, this.buurt)
  },
  watch: {
    geojson (to, from) {
      if (to.features.length) {
        this.updateLayer()
      }
    }
  },
  methods: {
    async updateLayer () {
      let geojsonLayer = this.geojsonLayer
      // Create a Leaflet geoJSON layer, or clear it
      if (!geojsonLayer) {
        geojsonLayer = L.geoJSON(null, {color: this.config.color}).addTo(this.map)
      } else {
        geojsonLayer.clearlayers()
      }
      geojsonLayer.addData(this.geojson)
      this.geojsonLayer = geojsonLayer
    }
  }
}
</script>

<style scoped>
</style>
