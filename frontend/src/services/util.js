import Vue from 'vue'
import { getToken } from './auth'

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

async function readPaginatedGeoJSON (url) {
  // Read data from a paginated GeoJSON endpoint
  // Note: distinct from normal JSON data because 'features' property must be accessed
  // .header("Authorization", "bearer " + token)

  const token = getToken()
  let next = url
  let results = {
    type: 'FeatureCollection',
    features: []
  }

  while (next) {
    try {
      let response = await Vue.axios.get(next, {
        headers: {
          Authorization: 'bearer ' + token
        }
      })
      next = response.data.next
      results.features = results.features.concat(response.data.results.features)
    } catch (e) {
      console.error('Request failed', e)
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
  let url = 'http://localhost:8000/gastransitie/api/afwc?buurt=' + buurt // TODO: fix hostname
  return readPaginatedGeoJSON(url)
}

export default {
  readPaginatedData,
  readData,
  loadCityData
}
