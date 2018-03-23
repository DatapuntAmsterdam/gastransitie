<template>
  <div id="app">
    <ams-header></ams-header>
    <ams-content>
      <router-view v-if="token"/>
      <div v-else>
        Deze pagina is alleen beschikbaar als u bent ingelogd.
      </div>
    </ams-content>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import header from './components/Header'
import content from './components/Content'

export default {
  name: 'App',
  components: {
    'ams-header': header,
    'ams-content': content
  },
  computed: {
    ...mapGetters([
      'token'
    ])
  }
}
</script>

<!-- Global styling -->
<style>
</style>
