import { getToken } from './auth'
import { readPaginatedData } from './datareader';

const LANDELIJK = 'LANDELIJK'
const VOLLCODE = 'VOLLCODE'

const GEOJSON = 'geojson'
const JSON = 'json'

const VOLLCODE2LANDELIJK = {}
const LANDELIJK2VOLLCODE = {}

const PRIVATE_URL = getConfigForHost().privateDataHost + '/gastransitie/api'
const NEIGHBORHOOD_WFS_URL = 'https://map.data.amsterdam.nl/maps/gebieden?REQUEST=GetFeature&SERVICE=wfs&Version=2.0.0&SRSNAME=EPSG:4326&typename=buurt_simple&outputformat=geojson'

// Cache keys are as follows: AREA.DATA_SETNAME where area is 'STAD' or a buurt identifier in VOLLCODE style
const DATASETS = {
  afwc: {
    download: (url, headers) => readPaginatedData(url, headers),
    getUrl: key => PRIVATE_URL + `/afwc/?buurt=${_translate(key, VOLLCODE)}`,
    getCacheKey: (datasetName, neighborhood) => `${_translate(neighborhood, VOLLCODE)}.${datasetName}`,
    postProcess: results => asGeojson(results),
    getHeaders: getDatapuntOAuthHeaders
  },
  energielabel: {
    download: (url, headers) => readPaginatedData(url, headers),
    getUrl: neighborhood => PRIVATE_URL + `/energielabel/?buurt=${_translate(neighborhood, VOLLCODE)}`,
    getCacheKey: (datasetName, neighborhood) => `${_translate(neighborhood, VOLLCODE)}.${datasetName}`,
    postProcess: results => asGeojson(results),
    getHeaders: getDatapuntOAuthHeaders
  },
  mip: {
    download: (url, headers) => readPaginatedData(url, headers),
    getUrl: neighborhood => PRIVATE_URL + `/mip/?buurt=${_translate(neighborhood, VOLLCODE)}`,
    getCacheKey: (datasetName, neighborhood) => `${_translate(neighborhood, VOLLCODE)}.${datasetName}`,
    postProcess: results => asGeojson(results),
    getHeaders: getDatapuntOAuthHeaders
  },
  renovatie: {
    download: (url, headers) => readPaginatedData(url, headers),
    getUrl: neighborhood => PRIVATE_URL + `/renovatie/?buurt=${_translate(neighborhood, VOLLCODE)}`,
    getCacheKey: (datasetName, neighborhood) => `${_translate(neighborhood, VOLLCODE)}.${datasetName}`,
    postProcess: results => asGeojson(results),
    getHeaders: getDatapuntOAuthHeaders
  },
  // buurtbounds is used to zoom in the various maps to the relevant neighborhood (factsheet page)
  buurtbounds: {
    download: (url, headers) => readPaginatedData(url, headers),
    getUrl: neighborhood => PRIVATE_URL + `/buurtbbox/?vollcode=${_translate(neighborhood, VOLLCODE)}`,
    getCacheKey: (datasetName, neighborhood) => `${_translate(neighborhood, VOLLCODE)}.${datasetName}`,
    postProcess: results => {
      let [W, S, E, N] = results.features[0].geometry
      return [[S, W], [N, E]]
    },
    getHeaders: getDatapuntOAuthHeaders
  },
  // allborders is used to draw borders on the small overall map on the neighborhood factsheet page
  allborders: {
    download: (url, headers) => get(url),
    getUrl: neighborhood => NEIGHBORHOOD_WFS_URL,
    getCacheKey: (datasetName, neighborhood) => `STAD.${datasetName}`,
    postProcess: results => results,
    getHeaders: () => {}
  },
  buurt: {
    download: (url, headers) => readPaginatedData(url, headers),
    getUrl: neighborhood => PRIVATE_URL + `/buurt/?vollcode=${_translate(neighborhood, VOLLCODE)}`,
    getCacheKey: (datasetName, neighborhood) => `${_translate(neighborhood, VOLLCODE)}.${datasetName}`,
    postProcess: results => asGeojson(results),
    getHeaders: getDatapuntOAuthHeaders
  },
  handelsregister: {
    download: (url, headers) => readPaginatedData(url, headers),
    getUrl: neighborhood => PRIVATE_URL + `/handelsregister/?buurt_id=${_translate(neighborhood, LANDELIJK)}`,
    getCacheKey: (datasetName, neighborhood) => `${_translate(neighborhood, VOLLCODE)}.${datasetName}`,
    postProcess: results => results,
    getHeaders: getDatapuntOAuthHeaders
  },
  handelsregisterbuurt: {
    download: (url, headers) => readPaginatedData(url, headers),
    getUrl: neighborhood => PRIVATE_URL + `/handelsregisterbuurt/?buurt_id=${_translate(neighborhood, LANDELIJK)}`,
    getCacheKey: (datasetName, neighborhood) => `${_translate(neighborhood, VOLLCODE)}.${datasetName}`,
    postProcess: results => results,
    headers: getDatapuntOAuthHeaders
  },
  warmtekoude: {
    download: (url, headers) => readPaginatedData(url, headers),
    getUrl: neighborhood => PRIVATE_URL + `/warmtekoude/`,
    getCacheKey: (datasetName, neighborhood) => `STAD.${datasetName}`,
    postProcess: results => asGeojson(results),
    getHeaders: getDatapuntOAuthHeaders
  },
  bagbrk: {
    download: (url, headers) => readPaginatedData(url, headers),
    getUrl: neighborhood => PRIVATE_URL + `/bag/${_translate(neighborhood, LANDELIJK)}/`,
    getCacheKey: (datasetName, neighborhood) => `${_translate(neighborhood, VOLLCODE)}.${datasetName}`,
    postProcess: async results => await results,
    getHeaders: getDatapuntOAuthHeaders
  },
  gasgroen: {
    download: (url, headers) => readPaginatedData(url, headers),
    getUrl: neighborhood => PRIVATE_URL + `/gasgroen/?buurt=${_translate(neighborhood, VOLLCODE)}`,
    getCacheKey: (datasetName, neighborhood) => `${_translate(neighborhood, VOLLCODE)}.${datasetName}`,
    postProcess: results => asGeojson(results),
    getHeaders: getDatapuntOAuthHeaders
  },
  gasoranje: {
    download: (url, headers) => readPaginatedData(url, headers),
    getUrl: neighborhood => PRIVATE_URL + `/gasoranje/?buurt=${_translate(neighborhood, VOLLCODE)}`,
    getCacheKey: (datasetName, neighborhood) => `${_translate(neighborhood, VOLLCODE)}.${datasetName}`,
    postProcess: results => asGeojson(results),
    getHeaders: getDatapuntOAuthHeaders
  },
  energie: {
    download: (url, headers) => readPaginatedData(url, headers),
    getUrl: neighborhood => PRIVATE_URL + `/energieverbruik/?vollcode=${_translate(neighborhood, VOLLCODE)}`,
    getCacheKey: (datasetName, neighborhood) => `${_translate(neighborhood, VOLLCODE)}.${datasetName}`,
    postProcess: results => results,
    getHeaders: getDatapuntOAuthHeaders
  }
}

/**
 * Create a valid GeoJSON Feature collection from an array of features.
 * @param {Array} features 
 */
function asGeojson (features) {
  return {
    type: 'FeatureCollection',
    features
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
 * Given a key of type vollcode or 
 * @param {string} key 
 * @param {string} keyType either 'VOLLCODE' or 'LANDELIJK' (but use the constants VOLLCODE or LANDELIJK)
 */
function _translate (key, keyType) {
  let translated = ''
  switch (key.length) {
    case 4: // we were provided a key of type VOLLCODE
      translated = (keyType === VOLLCODE) ? key : VOLLCODE2LANDELIJK[key]
    case 14: // we were provided a key of type LANDELIJK
      translated = (keyType === LANDELIJK) ? key : LANDELIJK2VOLLCODE[key]
    default:
      throw new Error('key type not "volledige code" or "landelijke code"')
  }
  return translated
}

//////////

async function accessData (datasetName, neighborhood) {
  // Access data set metadata
  let meta = DATASETS[datasetName]

  let getData = async () => {
    const url = meta.getUrl(neighborhood)
    const headers = meta.getHeaders()

    let download = meta.download ? meta.download : readPaginatedData // allow override of Paginated HAL-JSON assumption
    let postProcess = meta.postProcess ? meta.postProcess // allow override "returned data are GeoJSON features" assumption


    return meta.postProcess(download(url, headers))
  }
  let cacheKey = meta.getCacheKey(datasetName, neighborhood)

  return cacheResponse(cacheKey, getData)
}

// om te gebruiken:

let data = await accessData('mip', 'A08d')