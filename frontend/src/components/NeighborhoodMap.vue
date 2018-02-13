<!-- This component sets up the neighborhood map and zooms to the current neighborhood -->
<!-- duplicate part of this for other map views TODO -->
<template>
  <div>
    <div class="map"></div>
    <afwc-map-layer v-if="map" :buurt="buurt" :map="map"></afwc-map-layer>
    <neighborhood-border-map-layer v-if="map" :buurt="buurt" :map="map" ></neighborhood-border-map-layer>
    <mip-map-layer v-if="map" :buurt="buurt" :map="map"></mip-map-layer>
  </div>
</template>

<script>
import L from 'leaflet'
import util from '../services/util'

// individual map layers:
import AfwcMapLayer from './AfwcMapLayer'
import NeighborhoodBorderLayer from './NeighborhoodBorderLayer'
import MipMapLayer from './MipMapLayer'

export default {
  props: [
    'buurt'
  ],
  data () {
    return {
      map: null
    }
  },
  components: {
    'afwc-map-layer': AfwcMapLayer,
    'neighborhood-border-map-layer': NeighborhoodBorderLayer,
    'mip-map-layer': MipMapLayer
  },
  mounted () {
    this.map = L.map(this.$el).setView([52.367653, 4.900877], 12)
    L.tileLayer('https://{s}.data.amsterdam.nl/topo_wm_zw/{z}/{x}/{y}.png', {
      minZoom: 11,
      maxZoom: 21,
      subdomains: ['t1', 't2', 't3', 't4'],
      attribution: 'Datapunt Amsterdam'
    }).addTo(this.map)
    if (this.buurt) {
      this.setMapBounds(this.buurt)
    }
  },
  watch: {
    buurt (to, from) {
      if (to) {
        // center map on correct neighborhood
        this.setMapBounds(to)
        // data refreshing is done by individual layer components ...
      }
    }
  },
  methods: {
    async setMapBounds (buurt) {
      // access the bounding box endpoint, set map bounds based on result
      const url = 'http://localhost:8000/gastransitie/api/buurtbbox/?vollcode=' + buurt
      let results = util.resultsAsGeoJSON(
        await util.readProtectedPaginatedData(url, util.getGeoJSONData, util.getNextPage)
      )
      let bbox = results.features[0].geometry
      let bounds = [[bbox[1], bbox[0]], [bbox[3], bbox[2]]]
      this.map.fitBounds(bounds)
    }
  }
}
</script>

<style scoped>
.map {
  height: 600px;
}
</style>
