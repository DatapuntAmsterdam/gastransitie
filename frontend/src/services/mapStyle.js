let styleFunctions = {}

export function getStyleFunction (name) {
  if (!styleFunctions[name]) {
    return null
  }
  return styleFunctions[name]
}

export function registerStyleFunction (name, callback) {
  styleFunctions[name] = callback
}

// register style callbacks for various data sets

function warmteKoudeStyle (feature) {
  let color = 'gray'
  if (feature.properties.type_net.includes('WARMTE')) {
    color = 'red'
  } else if (feature.properties.type_net.includes('KOUDE')) {
    color = 'blue'
  }

  return {
    color: color,
    fillColor: 'none'
  }
}

registerStyleFunction('warmtekoude', warmteKoudeStyle)

function afwcStyle (feature) {
  let color = 'blue'
  if (feature.properties.corp === 'YMERE') {
    color = 'blue'
  }

  return {
    color: color,
    fillColor: color,
    fillOpacity: 0.7,
    weight: 2
  }
}

registerStyleFunction('afwc', afwcStyle)

function energieLabelStyle (feature) {
  let color = 'gray'
  switch (feature.properties.energielabel) {
    case 'A':
      color = 'rgb(14,152,19)'
      break
    case 'B':
      color = 'rgb(56,223,34)'
      break
    case 'C':
      color = 'rgb(180,254,78)'
      break
    case 'D':
      color = 'rgb(255,255,53)'
      break
    case 'E':
      color = 'rgb(254,209,78)'
      break
    case 'F':
      color = 'rgb(254,130,38)'
      break
    case 'G':
      color = 'rgb(223,22,27)'
      break
    default:
      color = 'gray'
  }

  return {
    color: color,
    stroke: false,
    fillColor: color,
    fillOpacity: 1,
    weight: 2
  }
}

registerStyleFunction('energielabel', energieLabelStyle)