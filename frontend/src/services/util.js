import Vue from 'vue'
import { getToken } from './auth'

// Helper function to access next link (used with readData)
const getNoNext = r => null
const getNextPage = r => r.data.next
const getNextPageHAL = r => r._links.next.href

const getNormalData = r => r.data
const getPaginatedData = r => r.data.results
const getGeoJSONData = r => r.data.results.features

// Access paginated resource
async function readPaginatedData (
  url,
  headers = {},
  getData = r => getPaginatedData,
  getNext = r => getNextPage
) {
  let next = url
  let results = []
  while (next) {
    try {
      let response = await Vue.axios.get(next, { headers })
      next = getNext(response)
      results = results.concat(getData(response))
    } catch (e) {
      console.error('Request failed', e)
      next = null
    }
  }
  return results
}

// Access OAuth2 protected paginated resource
async function readProtectedPaginatedData (
  url,
  getData = r => getPaginatedData,
  getNext = r => getNextPage
) {
  const token = getToken()
  if (token) {
    const results = await readPaginatedData(
      url, {
        Authorization: 'bearer ' + token
      },
      getData,
      getNext
    )
    return results
  } else {
    return []
  }
}

/* function resultsAsGeoJSON (features) {
  if (features.length) {
    return {
      type: 'FeatureCollection',
      features
    }
  } else {
    return {}
  }
} */

function resultsAsGeoJSON (features) {
  return {
    type: 'FeatureCollection',
    features
  }
}

async function loadCityData (buurt) {
  const url = 'http://localhost:8000/gastransitie/api/afwc/?buurt=' + buurt

  return resultsAsGeoJSON(
    await readProtectedPaginatedData(url, getGeoJSONData, getNextPage)
  )
}

async function loadBbox (buurt) {
  const url = 'http://localhost:8000/gastransitie/api/buurtbbox/?vollcode=' + buurt
  return resultsAsGeoJSON(
    await readProtectedPaginatedData(url, getGeoJSONData, getNextPage)
  )
}

async function loadBuurten () {
  const url = 'http://localhost:8000/gastransitie/api/buurt/'
  let results = await readProtectedPaginatedData(
    url,
    getGeoJSONData,
    getNextPage
  )
  let tmp = results.map(function (d, i) {
    return {
      vollcode: d.properties.vollcode,
      naam: d.properties.naam,
      landelijk: d.id
    }
  })
  tmp.sort(function (a, b) {
    if (a.naam > b.naam) {
      return +1
    } else if (a.naam < b.naam) {
      return -1
    } else {
      return 0
    }
  })
  return tmp
}

async function readData (url) {
  let response = await Vue.axios.get(url)
  return response.data
}

export default {
  readPaginatedData,
  readProtectedPaginatedData,
  readData,
  loadCityData,
  loadBbox,
  loadBuurten,
  resultsAsGeoJSON,
  // helper functions:
  getNoNext,
  getNextPage,
  getNextPageHAL,
  getNormalData,
  getPaginatedData,
  getGeoJSONData
}
