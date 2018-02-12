<template>
  <div class="map">AFWC 2017 kaart</div>
</template>

<script>
import L from 'leaflet'
import { mapGetters } from 'vuex'

export default {
  created () {
    this.vars = {
      map: null,
      tileLayer: null,
      dataLayer: null,
      mapControl: null
    }
  },
  computed: {
    ...mapGetters(['cityData', 'bbox'])
  },
  methods: {
    showMap () {
      let map = L.map(this.$el).setView([52.367653, 4.900877], 12)
      let tileLayer = L.tileLayer('https://{s}.data.amsterdam.nl/topo_wm/{z}/{x}/{y}.png', {
        minZoom: 11,
        maxZoom: 21,
        subdomains: ['t1', 't2', 't3', 't4'],
        attribution: 'Datapunt Amsterdam'
      }).addTo(map)
      let dataLayer = L.geoJSON().addTo(map)

      let baseLayers = {tileLayer}
      let overLays = {'AFWC data': dataLayer}

      L.control.layers(baseLayers, overLays, {hideSingleBase: true, collapsed: false}).addTo(map)

      // Save map and layer references to the local state of this component:
      this.vars.map = map
      this.vars.tileLayer = tileLayer
      this.vars.dataLayer = dataLayer
    }
  },
  mounted () {
    this.showMap()
  },
  watch: {
    cityData (to, from) {
      // Show the GeoJSON features that were loaded:
      if (to.hasOwnProperty('features')) {
        this.vars.dataLayer.addData(to)
      }
    },
    bbox (to, from) {
      if (to !== null) {
        // Django GIS extent and Leaflet bounds differ, hence:
        let bounds = [[to[1], to[0]], [to[3], to[2]]]
        this.vars.map.fitBounds(bounds)
      }
    }
  }
}
</script>

<style scoped>
.map {
  height: 800px;
}
</style>
