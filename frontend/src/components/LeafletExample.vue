<template>
  <div class="map">LEAFLET</div>
</template>

<script>
import L from 'leaflet'

export default {
  created () {
    console.log('Geen errors?')
  },
  mounted () {
    let map = L.map(this.$el).setView([51.505, -0.09], 13)
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map)
  }
}
</script>

<style scoped>
.map {height: 400px}
</style>
