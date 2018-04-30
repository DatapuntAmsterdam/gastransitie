// Handle all local geojson endpoints
// Handle extracting data (for tables)
import { getConfigForHost } from './hostConfig'
import { getDataByName } from './datasets'

// geoJson cache, keyed by "buurt" (lives outside of Vuex)
const PRIVATE_DATA_HOST = getConfigForHost().privateApiHost

async function getJsonByName (name, buurt) {
  // use new unified data handling system:
  return getDataByName(name, buurt)
}

export default {
  getJsonByName,
  PRIVATE_DATA_HOST
}
