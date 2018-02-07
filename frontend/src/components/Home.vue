<template>
  <div>
    <oauth></oauth>
    <factsheet v-if="token"></factsheet>
    <p>
      Please login to continue...
    </p>
  </div>
</template>

<script>
import { getToken } from '../services/auth'
import oauth from './OAuth'
import factsheet from './FactsheetPage'

export default {
  name: 'Home',
  components: {
    'oauth': oauth,
    'factsheet': factsheet
  },
  data () {
    return {
      token: null
    }
  },
  created () {
    this.token = getToken()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
