<!--
Map component for GeoJSON data sets, uses AmsterdamMapLayer(s) internally to display data.

This component handles the Leaflet instance, Leaflet settings and tile layer background layer.

See the mounted() callback below for an explanation of the supported keys for the config object.
-->
<template>
  <div>
    <div class="map"></div>
    <map-layer
      v-for="layerconfig in config.layers"
      v-bind:key="layerconfig.dataset"
      :config="layerconfig"
      :map="map"
      :v-if="map && buurt"
      :buurt="buurt">
    </map-layer>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

import L from 'leaflet'
import MapLayer from '@/components/AmsterdamMapLayer'
import datasets from '@/services/privatedatasets'

export default {
  props: [
    'config'
  ],
  data () {
    return {
      map: null
    }
  },
  computed: {
    ...mapGetters([
      'buurt'
    ])
  },
  components: {
    'map-layer': MapLayer
  },
  async mounted () {
    // Set basic Leaflet options to show most of Amsterdam, override with config.leafletBaseOptions if defined.
    // For config.leafletBaseOptions see the Leaflet documentation of map object:
    // http://leafletjs.com/reference-1.3.0.html#map
    const baseOptions = {
      attributionControl: false,
      zoomControl: true,
      scrollWheelZoom: false,
      center: [52.367653, 4.900877],
      zoom: 11,
      ...this.config.leafletBaseOptions
    }

    // Create a Leaflet instance and save a reference to it
    this.map = L.map(this.$el.querySelector('.map'), baseOptions)

    // If a wms tile background is defined, add it to the map.
    // See leaflet docs: http://leafletjs.com/reference-1.3.0.html#tilelayer for config.wms.settings
    // TODO: fix naming of "wms" config option (should be tiles or something close)
    if (this.config.wms) {
      L.tileLayer(this.config.wms.url, this.config.wms.settings).addTo(this.map)
    }

    let zoomOut = this.config.zoomOut
    const afterZoom = () => {
      if (zoomOut) {
        this.map.zoomOut(zoomOut)
        zoomOut = null
      }
    }
    this.map.on('zoomend', afterZoom)

    // The map will recenter on the current neighborhood unless the config.noZoom config property it set.
    if (this.buurt && !this.config.noZoom) {
      await this.setMapBounds()
    }
  },
  methods: {
    async setMapBounds () {
      const bounds = await datasets.getJsonByName('buurtbounds', this.buurt)
      return this.map.fitBounds(bounds)
    }
  },
  watch: {
    'buurt': function () {
      this.setMapBounds()
    }
  }
}
</script>

<style lang="scss" scope>
.map {
  height: 400px;
}
</style>
