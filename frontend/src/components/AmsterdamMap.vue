<!-- This component sets up the neighborhood map and zooms to the current neighborhood -->
<!-- duplicate part of this for other map views TODO -->
<template>
  <div>
    <div class="map"></div>
    <neighborhood-border-map-layer v-if="map" :buurt="buurt" :map="map" ></neighborhood-border-map-layer>
  </div>
</template>

<script>
import L from 'leaflet'

// individual map layers:
import NeighborhoodBorderLayer from './NeighborhoodBorderLayer'

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
    'neighborhood-border-map-layer': NeighborhoodBorderLayer
  },
  mounted () {
    this.map = L.map(this.$el, {
      attributionControl: false,
      preferCanvas: true,
      dragging: false,
      zoomControl: false
    }).setView([52.367653, 4.900877], 12)
    L.tileLayer('https://{s}.data.amsterdam.nl/topo_wm_zw/{z}/{x}/{y}.png', {
      minZoom: 11,
      maxZoom: 21,
      subdomains: ['t1', 't2', 't3', 't4']
    }).addTo(this.map)
  }
}
</script>

<style scoped>
.map {
  height: 400px;
}
</style>
