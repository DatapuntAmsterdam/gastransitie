<!-- component that shows MIP 2016 data layer up to date -->
<template>
  <div></div>
</template>

<script>
import L from 'leaflet'
import util from '../services/util'

const layerStyle = {
  color: 'red',
  fillColor: 'none',
  weight: 1
}

export default {
  props: [
    'map',
    'buurt'
  ],
  data () {
    return {
      geoJSONLayer: null
    }
  },
  mounted () {
    console.log('Mounted MIP 2016 layer')
    if (this.geoJSONLayer !== null) {
      console.log('Unexpected: we alreay have a geoJSONLayer')
    } else {
      this.geoJSONLayer = L.geoJSON(null, {style: layerStyle}).addTo(this.map)
    }
    if (this.buurt) {
      this.updateLayer(this.buurt)
    }
  },
  watch: {
    buurt (to, from) {
      this.updateLayer(to)
    }
  },
  methods: {
    async updateLayer (buurt) {
      const url = 'http://localhost:8000/gastransitie/api/mip/?buurt=' + buurt
      const results = await util.readProtectedPaginatedData(
        url,
        util.getGeoJSONData,
        util.getNextPage
      )
      let data = util.resultsAsGeoJSON(results)

      // update GeoJSON layer ...
      this.geoJSONLayer.clearLayers()
      if (data.features.length) {
        this.geoJSONLayer.addData(data)
      }
    }
  }
}
</script>

<style>
</style>
