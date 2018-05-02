import { getDataByName } from './datasets'

async function loadBuurten () {
  let results = await getDataByName('BOOTSTRAP', 'DOES NOT MATTER')
  return results.features.map(d => ({
    vollcode: d.properties.vollcode,
    naam: d.properties.naam,
    landelijk: d.id
  })).sort(
    (a, b) => (a.naam === b.naam) ? 0 : ((a.naam > b.naam) ? 1 : -1)
  )
}

const filteredText = (text, filterText) => {
  // $& Inserts the matched substring
  return filterText ? text.replace(RegExp(filterText, 'ig'), `<span class="filterText">$&</span>`) : text
}

export default {
  loadBuurten,
  filteredText
}
