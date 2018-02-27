<template>
  <div>
    <div class="map" style="height:400px"></div>
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
import L from 'leaflet'
import MapLayer from '@/components/AmsterdamMapLayer'
import datasets from '@/services/privatedatasets'

export default {
  props: [
    'config',
    'buurt'
  ],
  data () {
    return {
      map: null
    }
  },
  components: {
    'map-layer': MapLayer
  },
  async mounted () {
    // TODO: make baseOptions configurable as well (just an override in JSON config files)
    const baseOptions = {
      attributionControl: false,
      zoomControl: false,
      center: [52.367653, 4.900877],
      zoom: 11
    }

    this.map = L.map(this.$el.querySelector('.map'), this.config.leafletBaseOptions || baseOptions)

    if (this.config.wms) {
      L.tileLayer(this.config.wms.url, this.config.wms.settings).addTo(this.map)
    }

    if (this.buurt && !this.config.noZoom) {
      this.setMapBounds(this.buurt)
    }
  },
  methods: {
    async setMapBounds (buurt) {
      const bounds = await datasets.getBuurtBounds(buurt)
      this.map.fitBounds(bounds)
    }
  },
  watch: {
    buurt (to, from) {
      if (to) {
        console.log('Map received new buurt', to)
        this.setMapBounds(to)
      }
    }
  }
}
</script>

<style>

</style>
