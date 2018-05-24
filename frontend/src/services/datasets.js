import { getToken } from './auth'
import { cacheResponse, cacheDelete } from './cache'
import { get, readData, readPaginatedData } from './datareader'
import { getConfigForHost } from './hostConfig'

const LANDELIJK = 'LANDELIJK'
const VOLLCODE = 'VOLLCODE'

const VOLLCODE2LANDELIJK = {}
const LANDELIJK2VOLLCODE = {}

const PRIVATE_URL = getConfigForHost().privateDataHost + '/gastransitie/api'
const NEIGHBORHOOD_WFS_URL = 'https://map.data.amsterdam.nl/maps/gebieden?REQUEST=GetFeature&SERVICE=wfs&Version=2.0.0&SRSNAME=EPSG:4326&typename=buurt_simple&outputformat=geojson'

// Listing of all data sets, do not access directly, instead, call ...
const DATASETS = {
  DEFAULT: {
    // Default case, is used as fallback, override by defining them for a specific dataset.

    // Default assumption; data set uses HAL-JSON pagination:
    download: readPaginatedData,
    // Default assumption; data set is cached at the neighborhood level:
    getCacheKey: (datasetName, neighborhood) => `${_translate(neighborhood, VOLLCODE)}.${datasetName}`,
    // Default assumption; data is GeoJSON:
    postProcess: results => asGeojson(results),
    // Default assumption: dataset endpoint uses OAuth2
    getHeaders: getDatapuntOAuthHeaders
    // Note: there is no default getUrl function!
  },
  BOOTSTRAP: {
    // To initialize the VOLLCODE <=> LANDELIJK neigborhood code mapping, that is used for all dataset
    // to translate between these neighborhood ids we must hit the endpoint /gastransitie/api/buurt/ .
    getUrl: () => PRIVATE_URL + '/buurt/',
    getCacheKey: () => 'BOOTSTRAP',
    postProcess: results => {
      // Initialize the mappings, then just return the results (untouched) for use in application
      // start-up (see main.js in root of this Vue project).
      results = asGeojson(results)
      results.features.forEach(item => {
        VOLLCODE2LANDELIJK[item.properties.vollcode] = item.id
        LANDELIJK2VOLLCODE[item.id] = item.properties.vollcode
      })

      return results
    }
  },
  afwc: {
    getUrl: neighborhood => PRIVATE_URL + `/afwc/?buurt=${_translate(neighborhood, VOLLCODE)}`
  },
  energielabel: {
    getUrl: neighborhood => PRIVATE_URL + `/energielabel/?buurt=${_translate(neighborhood, VOLLCODE)}`
  },
  mip: {
    getUrl: neighborhood => PRIVATE_URL + `/mip/?buurt=${_translate(neighborhood, VOLLCODE)}`
  },
  renovatie: {
    getUrl: neighborhood => PRIVATE_URL + `/renovatie/?buurt=${_translate(neighborhood, VOLLCODE)}`
  },
  // buurtbounds is used to zoom in the various maps to the relevant neighborhood (factsheet page)
  buurtbounds: {
    getUrl: neighborhood => PRIVATE_URL + `/buurtbbox/?vollcode=${_translate(neighborhood, VOLLCODE)}`,
    postProcess: results => {
      results = asGeojson(results)
      let [W, S, E, N] = results.features[0].geometry
      return [[S, W], [N, E]]
    }
  },
  // allborders is used to draw borders on the small overall map on the neighborhood factsheet page
  allborders: {
    download: async (url, headers) => get(url),
    getUrl: neighborhood => NEIGHBORHOOD_WFS_URL,
    getCacheKey: (datasetName, neighborhood) => `STAD.${datasetName}`,
    postProcess: results => results.data,
    getHeaders: () => {}
  },
  buurt: {
    getUrl: neighborhood => PRIVATE_URL + `/buurt/?vollcode=${_translate(neighborhood, VOLLCODE)}`
  },
  handelsregister: {
    getUrl: neighborhood => PRIVATE_URL + `/handelsregister/?buurt_id=${_translate(neighborhood, LANDELIJK)}`,
    postProcess: results => results
  },
  handelsregisterbuurt: {
    getUrl: neighborhood => PRIVATE_URL + `/handelsregisterbuurt/?buurt_id=${_translate(neighborhood, LANDELIJK)}`,
    postProcess: results => results
  },
  warmtekoude: {
    getUrl: neighborhood => PRIVATE_URL + `/warmtekoude/`,
    getCacheKey: (datasetName, neighborhood) => `STAD.${datasetName}`
  },
  bagbrk: {
    download: readData,
    getUrl: neighborhood => PRIVATE_URL + `/bag/${_translate(neighborhood, LANDELIJK)}/`,
    postProcess: async results => results
  },
  gasgroen: {
    getUrl: neighborhood => PRIVATE_URL + `/gasgroen/?buurt=${_translate(neighborhood, VOLLCODE)}`
  },
  gasoranje: {
    getUrl: neighborhood => PRIVATE_URL + `/gasoranje/?buurt=${_translate(neighborhood, VOLLCODE)}`
  },
  energie: {
    getUrl: neighborhood => PRIVATE_URL + `/energieverbruik/?vollcode=${_translate(neighborhood, VOLLCODE)}`,
    postProcess: results => results
  }
}

/**
 * Create a valid GeoJSON Feature collection from HAL-JSON style GeoJSON endpoint output.
 * @param {Array} features
 */
function asGeojson (results) {
  return {
    type: 'FeatureCollection',
    features: results.reduce((a, b) => a.concat(b.features), [])
  }
}

/**
 * Get authorization headers provided the user is logged in, otherwise empty headers are returned.
 */
function getDatapuntOAuthHeaders () {
  const token = getToken()
  if (token) {
    return {Authorization: 'bearer ' + token}
  }
  return {}
}

/**
 * Access data set by name, either from cache or by downloading it from the API source.
 * @param {string} datasetName Name of the dataset
 * @param {string} neighborhood Neighborhood identifier (of type VOLLCODE, or LANDELIJK)
 * @param {Boolean} isRecursive flag that is used by initialization code, no public use
 */
export async function getDataByName (datasetName, neighborhood, isRecursive = false) {
  // First data access will do an extra request to populate the VOLLCODE <==> LANDELIJK
  // mappings, subsequent data access will hit the cache.
  if (!isRecursive) {
    await getDataByName('BOOTSTRAP', 'DOES NOT MATTER', true)
  }

  let meta = DATASETS[datasetName]
  let fallback = DATASETS.DEFAULT

  let getData = async () => {
    const url = meta.getUrl(neighborhood)
    const headers = (meta.getHeaders || fallback.getHeaders)()
    // const rawData = await (meta.download || fallback.download)(url, headers)
    const rawData = await (meta.download || fallback.download)(url, headers)
    const data = (meta.postProcess || fallback.postProcess)(rawData)
    return data
  }

  let key = (meta.getCacheKey || fallback.getCacheKey)(datasetName, neighborhood)
  return cacheResponse(key, getData)
}

/**
 * Remove data cached at the neighborhood level
 * @param {string} datasetName name of dataset
 * @param {string} neighborhood neighborhood identifier (of type VOLLCODE, or LANDELIJK)
 */
export async function removeData (datasetName, neighborhood) {
  let meta = DATASETS[datasetName]
  let fallback = DATASETS.DEFAULT

  const cacheKey = (meta.getCacheKey || fallback.getCacheKey)(datasetName, neighborhood)
  if (cacheKey.includes(neighborhood)) {
    // only reset cache for dataset that is keyed by neighborhood - do not re-download citywide data
    cacheDelete(cacheKey)
  }
}

/**
 * Given a key of type VOLLCODE or LANDELIJK translate it to desired type
 * @param {string} key neighborhood identifier (of type VOLLCODE or LANDELIJK)
 * @param {string} keyType desired type of neighborhood identifier (either VOLLCODE or LANDELIJK)
 */
function _translate (key, keyType) {
  let translated = ''
  switch (key.length) {
    case 4: // we were provided a key of type VOLLCODE
      translated = (keyType === VOLLCODE) ? key : VOLLCODE2LANDELIJK[key]
      break
    case 14: // we were provided a key of type LANDELIJK
      translated = (keyType === LANDELIJK) ? key : LANDELIJK2VOLLCODE[key]
      break
    default:
      throw new Error('key type not "volledige code" or "landelijke code"')
  }
  return translated
}
