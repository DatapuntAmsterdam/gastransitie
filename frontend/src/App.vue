<template>
  <div>
    <div class="header">
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

    <!--<loading-component></loading-component>-->
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import header from './components/Header'
import menu from './components/Menu'
import content from './components/Content'
import footer from './components/Footer'

export default {
  name: 'App',
  components: {
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

.header {

}

.footer {
  min-height: 226px;
}
</style>
