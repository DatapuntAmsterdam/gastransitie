<template>
  <div>
    <oauth></oauth>
    <refactor-map :config="afwcMapConfig" :buurt="buurt"></refactor-map>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import OAuth from './OAuth'

import RefactorMap from './RefactorMap'
import afwcMapConfig from '../../static/afwc-map-config'

export default {
  data () {
    return {
      buurt: this.$route.params.buurt,
      afwcMapConfig
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
