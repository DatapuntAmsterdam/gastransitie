<!--
Leaflet GeoJSON map layer, to be used with the AmsterdamMap.vue component.

This component is passed a config (a layer config from our custom Map config
files), a Leaflet map instance to draw on, and an Amsterdam neighborhood
represented by its "volledige code" like "A08d".

A layer config object is can contains the following keys:
"dataset": the name of the dataset (defined in datasets service)
"color": single color to use for this layer's GeoJSON data
"styleFunction": a callback that returns the style for a feature in the dataset
-->
<template>
  <div></div>
</template>

<script>
import L from 'leaflet'
import { getDataByName } from '../services/datasets'
import { getStyleFunction } from '@/services/mapStyle'

export default {
  props: [
    'config',
    'map',
    'buurt'
  ],
  data () {
    return {
      geojson: {type: 'FeatureCollection', features: []}, // placeholder GeoJSON data
      geojsonLayer: null
    }
  },
  async mounted () {
    console.assert(this.config !== null && this.config !== undefined, 'A config entry is needed to render this layer.')
    this.geojson = await getDataByName(this.config.dataset, this.buurt)
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

      // Remove existing GeoJSON map layer (if present)
      if (geojsonLayer) {
        this.map.removeLayer(geojsonLayer)
      }

      // Retrieve style callback for this layer/dataset (if defined in config)
      let styleFunction = null
      if (this.config.styleFunction) {
        styleFunction = getStyleFunction(this.config.styleFunction)
      }

      // Set layer style (either fixed color, or style callback function)
      if (!styleFunction) {
        geojsonLayer = L.geoJSON(null, {color: this.config.color}).addTo(this.map)
      } else {
        geojsonLayer = L.geoJSON(null, {style: styleFunction}).addTo(this.map)
      }

      // update map with new GeoJSON layer and save a reference to it
      geojsonLayer.addData(this.geojson)
      this.geojsonLayer = geojsonLayer
    }
  }
}
</script>

<style scoped>
</style>
