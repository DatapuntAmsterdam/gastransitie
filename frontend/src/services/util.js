import Vue from 'vue'
import { getToken } from './auth'

async function readPaginatedData (url, headers = {}, getData = r => r.data.results) {
  let next = url
  let results = []
  while (next) {
    try {
      let response = await Vue.axios.get(next, { headers })
      next = response.data.next
      results = results.concat(getData(response))
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
  const token = getToken()
  if (token) {
    const url = 'http://localhost:8000/gastransitie/api/afwc/?buurt=' + buurt // TODO: fix hostname
    const features = await readPaginatedData(
      url, {
        Authorization: 'bearer ' + token
      },
      r => r.data.results.features
    )
    return {
      type: 'FeatureCollection',
      features
    }
  } else {
    return {}
  }
}

async function loadBbox (buurt) {
  const token = getToken()
  if (token) {
    const url = 'http://localhost:8000/gastransitie/api/buurtbbox/?vollcode=' + buurt
    const features = await readPaginatedData(
      url, {
        Authorization: 'bearer ' + token
      },
      r => r.data.results.features
    )
    return {
      type: 'FeatureCollection',
      features
    }
  } else {
    return {}
  }
}

export default {
  readPaginatedData,
  readData,
  loadCityData,
  loadBbox
}
