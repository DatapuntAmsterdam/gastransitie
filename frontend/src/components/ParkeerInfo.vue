<template>
  <div v-if="ParkeerData">
    <div class="tableHeader">Parkeervakken</div>

    <table class="table table-hover table-responsive">
      <tbody>
        <tr>
          <td>Aantal vakken:</td>
          <td>{{ParkeerData.totaal}}</td>
        </tr>
        <tr>
          <td>Aantal laadplaatsen:</td>
          <td>{{ParkeerData.elektrisch}}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { getParkeerCounts } from '../services/parkeervakken'

export default {
  computed: {
    ...mapGetters([
      'buurt'
    ])
  },
  watch: {
    'buurt': function () {
      this.setParkeerCounts()
    }
  },
  data () {
    return {
      ParkeerData: {}
    }
  },
  created () {
    this.setParkeerCounts()
  },
  methods: {
    async setParkeerCounts (buurt) {
      this.ParkeerData = await getParkeerCounts(this.buurt)
    }
  }
}

</script>
