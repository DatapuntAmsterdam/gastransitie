import { get } from './datareader'
import { getToken } from './auth'
import privateDataSets from './privatedatasets'

// Helper function to access next link (used with readData)
const getNoNext = r => null
const getNextPage = r => r.data.next
const getNextPageHAL = r => r.data._links.next.href

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
    let requestedUrl = next
    try {
      let response = await get(next, { headers })
      next = getNext(response)
      results = results.concat(getData(response))
    } catch (e) {
      next = null
      console.log('Failure while accessing', requestedUrl)
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
    getNextPageHAL
  )
  return results.map(d => ({
    vollcode: d.properties.vollcode,
    naam: d.properties.naam,
    landelijk: d.id
  })).sort(
    (a, b) => (a.naam === b.naam) ? 0 : ((a.naam > b.naam) ? 1 : -1)
  )
}

async function readData (url) {
  let response = await get(url)
  return response.data
}

async function readProtectedData (url) {
  const token = getToken()
  let headers = {
    Authorization: 'bearer ' + token
  }
  let response = await get(
    url, { headers }
  )
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
  readProtectedData,
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
