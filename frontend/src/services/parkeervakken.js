import { readData } from '@/services/datareader'

// Todo: load asynchronously instead of sequentially
export async function getParkeerCounts (buurt) {
  let ParkeerData = {}
  const urlev = `https://api.data.amsterdam.nl/parkeervakken/parkeervakken/?buurtcode=${buurt}&bord=Opladen+elektrische+voertuigen`
  const data = await readData(urlev)
  ParkeerData['elektrisch'] = data.count

  const urltotaal = `https://api.data.amsterdam.nl/parkeervakken/parkeervakken/?buurtcode=${buurt}`
  const data2 = await readData(urltotaal)
  ParkeerData['totaal'] = data2.count

  return ParkeerData
}
