<template>
  <div>
    <oauth></oauth>
    <refactor-map :config="afwcMapConfig" :buurt="buurt"></refactor-map>
    <refactor-map :config="mipMapConfig" :buurt="buurt"></refactor-map>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import OAuth from './OAuth'

import RefactorMap from './RefactorMap'
import afwcMapConfig from '../../static/afwc-map-config'
import mipMapConfig from '../../static/mip-map-config'

export default {
  data () {
    return {
      buurt: this.$route.params.buurt,
      afwcMapConfig,
      mipMapConfig
    }
  },
  components: {
    'refactor-map': RefactorMap,
    'oauth': OAuth
  },
  methods: {
    ...mapActions({
      setBuurt: 'setBuurt'
    })
  },
  watch: {
    '$route' (to, from) {
      this.buurt = to.params.buurt
      this.setText()
    }
  }
}
</script>

<style scoped>
</style>
