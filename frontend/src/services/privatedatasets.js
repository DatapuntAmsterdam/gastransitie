// Handle all local geojson endpoints
// Handle extracting data (for tables)
import util from './util'

// general data
let buurtCache = {}
let buurtBoundsCache = {}

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
  if (!afwcCache[buurt]) {
    afwcCache[buurt] = readGeojson(getUrl('/afwc/') + `?buurt=${buurt}`)
  }
  return afwcCache[buurt]
}

async function getEnergieLabel (buurt) {
  if (!energieLabelCache[buurt]) {
    energieLabelCache[buurt] = readGeojson(getUrl('/energielabel/') + `?buurt=${buurt}`)
  }
  return energieLabelCache[buurt]
}

async function getMip (buurt) {
  if (!mipCache[buurt]) {
    mipCache[buurt] = readGeojson(getUrl('/mip/') + `?buurt=${buurt}`)
  }
  return mipCache[buurt]
}

async function getRenovatie (buurt) {
  if (!renovatieCache[buurt]) {
    renovatieCache[buurt] = readGeojson(getUrl('/renovatie/') + `?buurt=${buurt}`)
  }
  return renovatieCache[buurt]
}

async function _getAllBuurtBounds () {
  // From Django GEOSGeometry.extent docs:  (xmin, ymin, xmax, ymax). I.e. (lon, lat) coordinates.
  // This project uses Leaflet which uses (lat, lon) coordinates.
  // So from Django we get [W, S, E, N] and Leaflet needs [S, W, N, E]
  let geojson = await readGeojson(getUrl('/buurtbbox/'))
  geojson.features.forEach(
    feature => {
      let [W, S, E, N] = feature.geometry
      buurtBoundsCache[feature.properties.vollcode] = [[S, W], [N, E]]
    }
  )
}

async function getBuurtBounds (buurt) {
  if (!buurtBoundsCache[buurt]) {
    await _getAllBuurtBounds()
  }
  return buurtBoundsCache[buurt]
}

async function getBuurt (buurt) {
  if (!buurtCache[buurt]) {
    buurtCache[buurt] = readGeojson(getUrl('/buurt/') + `?vollcode=${buurt}`)
  }
  return buurtCache[buurt]
}

async function getGeojsonByName (name, buurt) {
  let getters = new Map([
    ['afwc', getAfwc],
    ['energielabel', getEnergieLabel],
    ['mip', getMip],
    ['renovatie', getRenovatie],
    ['buurtbounds', getBuurtBounds],
    ['buurt', getBuurt]
  ])

  return getters.get(name)(buurt)
}

export default {
  getAfwc,
  getEnergieLabel,
  getMip,
  getRenovatie,
  getGeojsonByName,
  getBuurtBounds,
  getBuurt
}
