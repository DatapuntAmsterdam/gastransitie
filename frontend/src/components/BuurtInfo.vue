<template>
  <div v-if="buurtData">
    <div class="tableHeader">Buurt</div>

    <table class="table table-hover table-responsive">
      <tbody>
      <tr>
        <td>Naam buurt:</td>
        <td>{{buurtData.naam}}</td>
      </tr>
        <tr>
          <td>Naam wijk:</td>
          <td>{{buurtData.buurtcombinatie.naam}}</td>
        </tr>
        <tr>
          <td>Naam stadsdeel:</td>
          <td>{{buurtData.stadsdeel.naam}}</td>
        </tr>
        <tr>
          <td>Buurtcode:</td>
          <td>{{buurtData.volledige_code}}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters([
      'buurtData'
    ])
  }
}
</script>
