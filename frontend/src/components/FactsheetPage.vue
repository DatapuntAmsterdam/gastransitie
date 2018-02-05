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
      dataLayer: null
    }
  },
  computed: {
    ...mapGetters(['cityData'])
  },
  methods: {
    showMap () {
      let map = L.map(this.$el).setView([52.367653, 4.900877], 12)
      L.tileLayer('https://{s}.data.amsterdam.nl/topo_wm_zw/{z}/{x}/{y}.png', {
        minZoom: 11,
        maxZoom: 21,
        subdomains: ['t1', 't2', 't3', 't4'],
        attribution: 'Datapunt Amsterdam'
      }).addTo(map)
      let dataLayer = L.geoJSON().addTo(map)

      // Save map and layer references to the local state of this component:
      this.vars.dataLayer = dataLayer
      this.vars.map = map
    }
  },
  mounted () {
    this.showMap()
  },
  watch: {
    cityData (to, from) {
      // Show the GeoJSON features that were loaded:
      this.vars.dataLayer.addData(to)
    }
  }
}
</script>

<style scoped>
.map {
  height: 800px;
}
</style>
