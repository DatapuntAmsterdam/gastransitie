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
  let color = 'gray'
  switch (feature.properties.corp) {
    case 'CORDAAN':
      color = 'rgb(99,98,97)'
      break
    case 'DEALLIANTIE':
      color = 'rgb(253,50,78)'
      break
    case 'DEGOEDEWONING':
      color = 'rgb(133,251,213)'
      break
    case 'DEKEY':
      color = 'rgb(216,151,75)'
      break
    case 'DUWO':
      color = 'rgb(149,42,124)'
      break
    case 'DUWOROCHDALE':
      color = 'rgb(70,180,215)'
      break
    case 'EIGENHAARD':
      color = 'rgb(237,143,211)'
      break
    case 'GOEDESTEDE':
      color = 'rgb(249,232,70)'
      break
    case 'HABION':
      color = 'rgb(214,230,86)'
      break
    case 'INTERMARIS':
      color = 'rgb(220,84,137)'
      break
    case 'PARTEON':
      color = 'rgb(165,82,219)'
      break
    case 'ROCHDALE':
      color = 'rgb(157,174,93)'
      break
    case 'SAMENWERKING':
      color = 'rgb(148,148,148)'
      break
    case 'STADGENOOT':
      color = 'rgb(48,217,77)'
      break
    case 'STADSHERSTEL':
      color = 'rgb(153,73,45)'
      break
    case 'WOONCOMPAGNIE':
      color = 'rgb(254,145,81)'
      break
    case 'WOONZORGNEDERLAND':
      color = 'rgb(47,158,118)'
      break
    case 'WORMERWONEN':
      color = 'rgb(201,193,252)'
      break
    case 'YMERE':
      color = 'rgb(80,117,189)'
      break
    case 'ZVH':
      color = 'rgb(205,110,94)'
      break
  }

  return {
    color: color,
    fillColor: color,
    fillOpacity: 0.7,
    weight: 2
  }
}

registerStyleFunction('afwc', afwcStyle)

export const LABELS = {
  'ENERGIE': {
    'A': {
      label: 'Zeer laag energieverbruik',
      color: 'rgb(14,152,19)'
    },
    'B': {
      label: 'Laag energieverbruik',
      color: 'rgb(56,223,34)'
    },
    'C': {
      label: 'Redelijk laag energieverbruik',
      color: 'rgb(180,254,78)'
    },
    'D': {
      label: 'Gemiddeld energieverbruik',
      color: 'rgb(255,255,53)'
    },
    'E': {
      label: 'Redelijk hoog energieverbruik',
      color: 'rgb(254,209,78)'
    },
    'F': {
      label: 'Hoog energieverbruik',
      color: 'rgb(254,130,38)'
    },
    'G': {
      label: 'Zeer hoog energieverbruik',
      color: 'rgb(223,22,27)'
    }
  }
}

const getColor = (labels, label) => (labels[label] && labels[label].color) || 'gray'

function energieLabelStyle (feature) {
  const color = getColor(LABELS.ENERGIE, feature.properties.energielabel)
  return {
    color,
    stroke: false,
    fillColor: color,
    fillOpacity: 1,
    weight: 2
  }
}

registerStyleFunction('energielabel', energieLabelStyle)

function allBordersStyle (feature) {
  return {
    color: 'black',
    fill: false,
    weight: 1
  }
}

registerStyleFunction('allborders', allBordersStyle)
