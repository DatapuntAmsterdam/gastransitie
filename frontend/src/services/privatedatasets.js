// Handle all local geojson endpoints
// Handle extracting data (for tables)
import util from './util'

/* // general data
let allBuurten = null */

// geoJson cache, keyed by "buurt" (lives outside of Vuex)
let afwcCache = {}
let mipCache = {}
let energieLabelCache = {}
let renovatieCache = {}

function getUrl (endpoint, buurt = null) {
  return `http://localhost:8000/gastransitie/api${endpoint}`
}

async function readGeojson (url) {
  const results = await util.readProtectedPaginatedData(
    url,
    util.getGeoJSONData,
    util.getNextPage
  )
  return util.resultsAsGeoJSON(results)
}

// Energie transitie specific data endpoints (all paginated GeoJSON)
async function getAfwc (buurt) {
  if (!afwcCache.hasOwnProperty(buurt)) {
    console.log('Downloading new data')
    const geojson = await readGeojson(getUrl('/afwc/') + `?buurt=${buurt}`)
    afwcCache[buurt] = geojson
  }
  return afwcCache[buurt]
}

async function getEnergieLabel (buurt) {
  if (!energieLabelCache.hasOwnProperty(buurt)) {
    const geojson = await readGeojson(getUrl('/energielabel/') + `?buurt=${buurt}`)
    energieLabelCache[buurt] = geojson
  }
  return energieLabelCache[buurt]
}

async function getMip (buurt) {
  if (!mipCache.hasOwnProperty(buurt)) {
    const geojson = await readGeojson(getUrl('/mip/') + `?buurt=${buurt}`)
    mipCache[buurt] = geojson
  }
  return mipCache[buurt]
}

async function getRenovatie (buurt) {
  if (!renovatieCache.hasOwnProperty(buurt)) {
    const geojson = await readGeojson(getUrl('/renovatie/') + `?buurt=${buurt}`)
    renovatieCache[buurt] = geojson
  }
  return renovatieCache[buurt]
}

async function getGeojsonByName (name, buurt) {
  let getters = new Map([
    ['afwc', getAfwc],
    ['energielabel', getEnergieLabel],
    ['mip', getMip],
    ['renovatie', getRenovatie]
  ])

  return getters.get(name)(buurt)
}

async function getBuurtBounds (buurt) {
  let geojson = await readGeojson(getUrl('/buurtbbox/') + `?vollcode=${buurt}`)
  let bbox = geojson.features[0].geometry
  return [[bbox[1], bbox[0]], [bbox[3], bbox[2]]]
}

export default {
  getAfwc,
  getEnergieLabel,
  getMip,
  getRenovatie,
  getGeojsonByName,
  getBuurtBounds
}
