<template>
  <div>
    <oauth></oauth>
    <factsheet></factsheet>
  </div>
</template>

<script>
import oauth from './OAuth'
import factsheet from './FactsheetPage'

export default {
  name: 'Home',
  components: {
    'oauth': oauth,
    'factsheet': factsheet
  },
  computed: {
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
