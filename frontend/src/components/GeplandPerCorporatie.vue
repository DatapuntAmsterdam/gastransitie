<template>
  <div>
    <div class="tableHeader">Geplande werkzaamheden per woningcorporatie</div>
    <table v-if="data && data.features.length" class="table table-hover table-responsive">
      <thead>
        <tr>
          <th v-for="c in Object.keys(corporaties)" :key="c">
            {{corporaties[c]}}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td v-for="c in Object.keys(corporaties)" :key="c">
            {{data.features[0].properties[c]}}
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

const corporaties = {
  alliantie: 'Alliantie',
  de_key: 'De Key',
  eigen_haar: 'Eigen Haard',
  rochdale: 'Rochdale',
  stadgenoot: 'Stadgenoot',
  ymere: 'Ymere'
}

export default {
  data () {
    return {
      data: null,
      corporaties
    }
  },
  computed: {
    ...mapGetters([
      'buurt'
    ])
  },
  created () {
    this.getData()
  },
  methods: {
    async getData () {
      if (this.buurt) {
        this.data = await datasets.getJsonByName('renovatie', this.buurt)
      }
    }
  },
  watch: {
    'buurt': function () {
      this.getData()
    }
  }
}
</script>

<style>
</style>
