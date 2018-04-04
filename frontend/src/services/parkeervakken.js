import util from './util'

// Todo: load asynchronously instead of sequentially

export async function getParkeerCounts (buurt) {
  let ParkeerData = {}
  const urlev = `https://api.data.amsterdam.nl/parkeervakken/parkeervakken/?buurtcode=${buurt}&bord=Opladen+elektrische+voertuigen`
  const data = await util.readData(urlev)
  ParkeerData['elektrisch'] = data.count

  const urltotaal = `https://api.data.amsterdam.nl/parkeervakken/parkeervakken/?buurtcode=${buurt}`
  const data2 = await util.readData(urltotaal)
  ParkeerData['totaal'] = data2.count

  return ParkeerData
}
