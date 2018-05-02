import { readData } from '@/services/datareader'

// Todo: load asynchronously instead of sequentially
export async function getBBGAVariables (vars, year, buurt) {
  let BBGAData = {}
  for (let variabele of vars) {
    const url = `https://api.data.amsterdam.nl/bbga/cijfers/?variabele=${variabele}&gebiedcode15=${buurt}&jaar=${year}`
    const data = await readData(url)
    if (data.count !== 1) {
      console.error('We received more than one result for variable, neighborhood, year combination')
    }
    BBGAData[variabele] = data.results[0].waarde
  }
  return BBGAData
}
