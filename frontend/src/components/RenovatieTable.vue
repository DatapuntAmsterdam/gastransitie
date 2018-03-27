<template>
  <div>
    <h3>Geplande werkzaamheden per woningcorporatie</h3>
    <table v-if="data && data.features.length" class="table table-hover">
      <thead>
        <tr>
          <th>Alliantie</th>
          <th>De Key</th>
          <th>Eigen Haard</th>
          <th>Rochdale</th>
          <th>Stadgenoot</th>
          <th>Ymere</th>
          <th>2017</th>
          <th>2018</th>
          <th>2019</th>
          <th>2020</th>
          <th>2021</th>
          <th>2022</th>
          <th>2023</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>{{data.features[0].properties.alliantie}}</td>
          <td>{{data.features[0].properties.de_key}}</td>
          <td>{{data.features[0].properties.eigen_haar}}</td>
          <td>{{data.features[0].properties.rochdale}}</td>
          <td>{{data.features[0].properties.stadgenoot}}</td>
          <td>{{data.features[0].properties.ymere}}</td>
          <td>{{data.features[0].properties.jaar_2017}}</td>
          <td>{{data.features[0].properties.jaar_2018}}</td>
          <td>{{data.features[0].properties.jaar_2019}}</td>
          <td>{{data.features[0].properties.jaar_2020}}</td>
          <td>{{data.features[0].properties.jaar_2021}}</td>
          <td>{{data.features[0].properties.jaar_2022}}</td>
          <td>{{data.features[0].properties.jaar_2023}}</td>
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
