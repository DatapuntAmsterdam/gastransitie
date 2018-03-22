<template>
  <div>
    <ams-header></ams-header>
    <div id="app" class="container-fluid">
      <router-view/>
    </div>
  </div>
</template>

<script>
import header from './components/Header'

export default {
  name: 'App',
  components: {
    'ams-header': header
  }
}
</script>

<!-- Global styling -->
<style>
</style>
