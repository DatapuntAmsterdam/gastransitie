<template>
  <div>
    <div>
      <ams-header :title="title"></ams-header>

      <div>
        <ams-menu>Menu</ams-menu>
      </div>
    </div>

    <div class="content">
      <ams-content>
        <router-view v-if="token"/>
        <div v-else>
          Deze pagina is alleen beschikbaar als u bent ingelogd.
        </div>
      </ams-content>
    </div>

    <div class="footer">
      <ams-footer :title="title"></ams-footer>
    </div>

    <loading-component></loading-component>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import header from './components/Layout/Header'
import menu from './components/Layout/Menu'
import content from './components/Layout/Content'
import footer from './components/Layout/Footer'
import LoadingComponent from './components/Layout/LoadingComponent'

export default {
  name: 'App',
  components: {
    LoadingComponent,
    'ams-header': header,
    'ams-menu': menu,
    'ams-content': content,
    'ams-footer': footer
  },
  computed: {
    ...mapGetters([
      'token'
    ])
  },
  data () {
    return {
      title: 'City Deal Energietransitie'
    }
  }
}
</script>

<!-- Global styling -->
<style scoped>
.content {
  min-height: calc(100vh - 348px);
}

.footer {
  min-height: 226px;
}
</style>
