let styleFunctions = {}

const getColor = (labels, label) => (labels[label] && labels[label].color) || 'gray'

export function getStyleFunction (name) {
  return styleFunctions[name]
}

export function registerStyleFunction (name, callback) {
  styleFunctions[name] = callback
}

// register style callbacks for various data sets

export const LABELS = {
  'CORPORATIE': {
    'CORDAAN': {
      label: 'Cordaan',
      color: 'rgb(99,98,97)'
    },
    'DEALLIANTIE': {
      label: 'De Alliantie',
      color: 'rgb(253,50,78)'
    },
    'DEGOEDEWONING': {
      label: 'De Goede Woning',
      color: 'rgb(133,251,213)'
    },
    'DEKEY': {
      label: 'De Key',
      color: 'rgb(216,151,75)'
    },
    'DUWO': {
      label: 'DUWO',
      color: 'rgb(149,42,124)'
    },
    'DUWOROCHDALE': {
      label: 'DUWO Rochdale',
      color: 'rgb(70,180,215)'
    },
    'EIGENHAARD': {
      label: 'Eigen Haard',
      color: 'rgb(237,143,211)'
    },
    'GOEDESTEDE': {
      label: 'Goede Stede',
      color: 'rgb(249,232,70)'
    },
    'HABION': {
      label: 'Habion',
      color: 'rgb(214,230,86)'
    },
    'INTERMARIS': {
      label: 'Intermaris',
      color: 'rgb(220,84,137)'
    },
    'PARTEON': {
      label: 'Parteon',
      color: 'rgb(165,82,219)'
    },
    'ROCHDALE': {
      label: 'Rochdale',
      color: 'rgb(157,174,93)'
    },
    'SAMENWERKING': {
      label: 'Samenwerking',
      color: 'rgb(148,148,148)'
    },
    'STADGENOOT': {
      label: 'Stadgenoot',
      color: 'rgb(48,217,77)'
    },
    'STADSHERSTEL': {
      label: 'Stadsherstel',
      color: 'rgb(153,73,45)'
    },
    'WOONCOMPAGNIE': {
      label: 'Wooncompagnie',
      color: 'rgb(254,145,81)'
    },
    'WOONZORGNEDERLAND': {
      label: 'Woonzorg Nederland',
      color: 'rgb(47,158,118)'
    },
    'WORMERWONEN': {
      label: 'Wormer Wonen',
      color: 'rgb(201,193,252)'
    },
    'YMERE': {
      label: 'Ymere',
      color: 'rgb(80,117,189)'
    },
    'ZVH': {
      label: 'ZVH',
      color: 'rgb(205,110,94)'
    }
  },
  'WARMTE': {
    'WARMTE TRANSPORT': {
      label: 'Warmte net',
      color: 'red'
    },
    'KOUDE TRANSPORT': {
      label: 'Koude net',
      color: 'blue'
    }
  },
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

function afwcStyle (feature) {
  const color = getColor(LABELS.CORPORATIE, feature.properties.corp)
  return {
    color,
    fillColor: color,
    fillOpacity: 0.7,
    weight: 2
  }
}

registerStyleFunction('afwc', afwcStyle)

function warmteKoudeStyle (feature) {
  const color = getColor(LABELS.WARMTE, feature.properties.type_net)
  return {
    color,
    fillColor: 'none'
  }
}

registerStyleFunction('warmtekoude', warmteKoudeStyle)

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
