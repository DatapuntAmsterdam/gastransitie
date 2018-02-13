<template>
  <div class="container-fluid">
    <oauth></oauth>
    <table v-if="buurten.length" class="table table-sm table-striped table-bordered">
      <thead>
        <tr>
          <th scope="col">Buurt</th>
          <th scope="col">vollcode</th>
          <th scope="col">Landelijke code</th>
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
    <div v-else>
      Loading...
    </div>
  </div>

</template>

<script>
import { mapGetters } from 'vuex'
import OAuth from './OAuth'

export default {
  computed: {
    ...mapGetters([
      'buurten'
    ])
  },
  components: {
    'oauth': OAuth
  }
}
</script>

<style scoped>
</style>
