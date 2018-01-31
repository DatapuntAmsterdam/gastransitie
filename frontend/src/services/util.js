import Vue from 'vue'

async function readPaginatedData (url) {
  let next = url
  let results = []
  while (next) {
    try {
      let response = await Vue.axios.get(next)
      next = response.data.next
      response.data.results.forEach(result => {
        results.push(result)
      })
    } catch (e) {
      next = null
    }
  }
  return results
}

async function readData (url) {
  let response = await Vue.axios.get(url)
  return response.data
}

async function loadCityData (buurt) {
  let url = 'http://localhost:8000/gastransitie/api/afwc/?buurt=' + buurt // TODO: fix hostname
  return readData(url) // is normal GeoJSON for now
}

export default {
  readPaginatedData,
  readData,
  loadCityData
}
