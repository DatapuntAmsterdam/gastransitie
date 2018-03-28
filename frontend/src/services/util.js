import Vue from 'vue'
import { getToken } from './auth'
import privateDataSets from './privatedatasets'

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

function resultsAsGeoJSON (features) {
  return {
    type: 'FeatureCollection',
    features
  }
}

async function loadBuurten () {
  const url = privateDataSets.PRIVATE_DATA_HOST + '/gastransitie/api/buurt/'
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

const filteredText = (text, filterText) => {
  // $& Inserts the matched substring
  return filterText ? text.replace(RegExp(filterText, 'ig'), `<span class="filterText">$&</span>`) : text
}

export default {
  readPaginatedData,
  readProtectedPaginatedData,
  readData,
  loadBuurten,
  resultsAsGeoJSON,
  // helper functions:
  getNoNext,
  getNextPage,
  getNextPageHAL,
  getNormalData,
  getPaginatedData,
  getGeoJSONData,
  filteredText
}
