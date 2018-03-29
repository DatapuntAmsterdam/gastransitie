<template>
  <div>
    <div class="tableHeader">Geplande werkzaamheden per jaar</div>
    <table v-if="data && data.features.length" class="table table-hover">
      <thead>
        <tr>
          <th v-for="y in years" :key="y">{{y}}</th>
        </tr>
      </thead>
      <tbody>
      <tr>
          <td v-for="y in years" :key="y">
            {{data.features[0].properties[`jaar_${y}`]}}
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>
      Geen gegevens beschikbaar
    </p>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

import datasets from '@/services/privatedatasets'

const startYear = (new Date()).getFullYear() - 1
const NYEARS = 7
const years = new Array(NYEARS).fill(0).map((i, n) => startYear + n)

export default {
  data () {
    return {
      data: null,
      years
    }
  },
  created () {
    this.getData()
  },
  computed: {
    ...mapGetters([
      'buurt'
    ])
  },
  methods: {
    async getData () {
      if (this.buurt) {
        this.data = await datasets.getJsonByName('renovatie', this.buurt)
      }
    }
  },
  watch: {
    buurt (to, from) {
      this.getData()
    }
  }
}
</script>

<style>

</style>
