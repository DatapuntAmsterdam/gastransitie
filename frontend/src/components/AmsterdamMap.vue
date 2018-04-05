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
    // TODO: make baseOptions configurable as well (just an override in JSON config files)
    const baseOptions = {
      attributionControl: false,
      zoomControl: true,
      scrollWheelZoom: false,
      center: [52.367653, 4.900877],
      zoom: 11,
      ...this.config.leafletBaseOptions
    }

    this.map = L.map(this.$el.querySelector('.map'), baseOptions)

    if (this.config.wms) {
      L.tileLayer(this.config.wms.url, this.config.wms.settings).addTo(this.map)
    }

    if (this.buurt && !this.config.noZoom) {
      await this.setMapBounds()
      const zoomOut = () => {
        if (this.config.zoomOut) {
          this.map.zoomOut(this.config.zoomOut)
        }
        this.map.off('zoomend', zoomOut)
      }
      this.map.on('zoomend', zoomOut)
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
