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

async function readProtectedPaginatedData (url, getData = r => r.data.results) {
  const token = getToken()
  if (token) {
    const results = await readPaginatedData(
      url, {
        Authorization: 'bearer ' + token
      },
      getData
    )
    return results
  } else {
    return []
  }
}

async function loadCityData (buurt) {
  const url = 'http://localhost:8000/gastransitie/api/afwc/?buurt=' + buurt
  const getData = r => r.data.results.features

  const features = await readProtectedPaginatedData(url, getData)
  if (features.length) {
    return {
      type: 'FeatureCollection',
      features
    }
  } else {
    return {}
  }
}

async function loadBbox (buurt) {
  const url = 'http://localhost:8000/gastransitie/api/buurtbbox/?vollcode=' + buurt
  const getData = r => r.data.results.features

  const features = await readProtectedPaginatedData(url, getData)
  if (features.length) {
    return {
      type: 'FeatureCollection',
      features
    }
  } else {
    return {}
  }
}

async function readData (url) {
  let response = await Vue.axios.get(url)
  return response.data
}

export default {
  readPaginatedData,
  readData,
  loadCityData,
  loadBbox
}
