<template>
  <div>
    <h2>Buurten</h2>

    <div v-if="buurten">
      <div class="form-group">
        <input v-model="filterText"
               type="text"
               id="formInput"
               class="form-control"
               placeholder="Filtertekst">

        <button type="button"
                class="btn btn-primary mt-1"
                :disabled="!filterText"
                @click="clearFilter()">
          Wis filter
        </button>
      </div>

      <table class="table table-hover">
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
            <router-link :to="{path: '/factsheet/' + buurt.vollcode}">
              <span v-html="filteredText(buurt.naam, filterText)"></span>
            </router-link>
          </td>
          <td v-for="attr in ['vollcode', 'landelijk']" :key="attr">
            <span v-html="filteredText(buurt[attr], filterText)"></span>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import util from '../../services/util'

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
    },

    filteredText: util.filteredText
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
