<template>
  <div>
    <table v-if="buurten" width="100%">
      <caption></caption>
      <thead>
      <tr>
        <th>Naam</th>
        <th>Code</th>
        <th>Landelijke code</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="buurt in buurten" :key="buurt.vollcode">
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
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters([
      'buurten'
    ])
  },
  components: {
  }
}
</script>

<style scoped>
</style>
