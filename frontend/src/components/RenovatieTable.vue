<template>
  <div>
    <h3>Geplande werkzaamheden per woningcorporatie</h3>
    <table>
      <thead>
        <tr>
          <th>Datum</th>
          <th>Organisatie</th>
          <th>Omschrijving</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>t</td>
          <td>b</td>
          <td>d</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import datasets from '@/services/privatedatasets'

export default {
  props: [
    'buurt'
  ],
  data () {
    return {
      data: null
    }
  },
  created () {
    this.getData()
  },
  methods: {
    async getData () {
      console.log('retreive?', this.buurt)
      if (this.buurt) {
        this.data = await datasets.getJsonByName('renovatie', this.buurt)
        console.log('Renovatie data set', this.data)
      }
    }
  },
  watch: {
    buurt (to, from) {
      this.getData()
    }
  }
}
</script>

<style>

</style>
