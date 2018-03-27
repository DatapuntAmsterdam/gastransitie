<template>
  <div>
    <ams-header>City Deal Aardgasloos</ams-header>

    <ams-menu>Menu</ams-menu>

    <ams-content>
      <router-view v-if="token"/>
      <div v-else>
        Deze pagina is alleen beschikbaar als u bent ingelogd.
      </div>
    </ams-content>

    <!--<ams-footer>Footer</ams-footer>-->

    <loading-component></loading-component>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import header from './components/Header'
import menu from './components/Menu'
import content from './components/Content'

export default {
  name: 'App',
  components: {
    'ams-header': header,
    'ams-menu': menu,
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
