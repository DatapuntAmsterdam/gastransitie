<template>
  <table v-if="buurten.length" class="table table-sm table-striped table-bordered">
    <thead>
      <tr>
        <th scope="col">Buurt</th>
        <th scope="col">vollcode</th>
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
      </tr>
    </tbody>
  </table>
  <div v-else>
    Loading...
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters([
      'buurten'
    ])
  }
}
</script>

<style scoped>
</style>
