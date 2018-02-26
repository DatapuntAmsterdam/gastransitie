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
    this.geojson = await datasets.getGeojsonByName(this.config.dataset, this.buurt)
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
      if (!geojsonLayer) {
        console.log('Adding a new layer to the map, storing a reference.')
        geojsonLayer = L.geoJSON(null).addTo(this.map)
      }
      geojsonLayer.addData(this.geojson)
      this.geojsonLayer = geojsonLayer
      console.assert(this.geojsonLayer, 'this.geojsonLayer is not defined')
    }
  }
}
</script>

<style scoped>
</style>
