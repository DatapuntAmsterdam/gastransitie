<template>
  <div>
    <div v-if="buurten">
      <div class="rij mode_input text rij_verplicht">
        <div class="invoer">
          <input v-model="filterText"
                 type="text"
                 id="formInput"
                 class="input"
                 placeholder="Filtertekst">
        </div>

        <button class="action primary" @click="clearFilter()">Clear</button>
      </div>
    <table width="100%">
      <caption></caption>
      <thead>
      <tr>
        <th>Naam</th>
        <th>Code</th>
        <th>Landelijke code</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="buurt in filteredList" :key="buurt.vollcode">
        <td>
          <router-link :to="{path: '/factsheet/' + buurt.vollcode}">{{buurt.naam}}</router-link>
        </td>
        <td>
          {{buurt.vollcode}}
        </td>
        <td>
          {{buurt.landelijk}}
        </td>
      </tr>
      </tbody>
    </table>
    </div>
    <div v-else>
      Laden...
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

const buurtText = v => ['naam', 'vollcode', 'landelijk'].map(key => v[key].toLowerCase()).join('.')

/**
 * autofilter timeout
 */
let autoFilter

export default {
  data () {
    return {
      filteredList: [],
      filterText: ''
    }
  },
  methods: {
    clearFilter () {
      this.filterText = ''
      this.filteredList = this.buurten
    },

    filter () {
      const filterText = this.filterText.toLowerCase()
      this.filteredList = this.buurten.filter(v => buurtText(v).includes(filterText))
    }
  },
  computed: {
    ...mapGetters([
      'buurten'
    ])
  },
  watch: {
    'buurten' () {
      this.clearFilter()
    },
    'filterText' () {
      if (autoFilter) {
        clearTimeout(autoFilter)
      }
      autoFilter = setTimeout(() => this.filter(), 250)
    }
  },
  created () {
    this.clearFilter()
  },
  components: {
  }
}
</script>

<style scoped>
</style>
