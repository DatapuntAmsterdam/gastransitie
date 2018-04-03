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
