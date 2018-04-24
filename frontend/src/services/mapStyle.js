// Service that provides pre-defined categorical color scales.
let styleFunctions = {}

/**
 * Get the color associated with a label, update its count.
 * @param {Object} labels labels is an object with colors and labels for a given dataset
 * @param {string} label
 */
const getColor = (labels, label) => {
  if (labels[label] && labels[label].color) {
    labels[label].count += 1
    return labels[label].color
  } else {
    return 'gray'
  }
}

/**
 * Get a style callback function for a given named data set.
 * @param {string} name
 */
export function getStyleFunction (name) {
  return styleFunctions[name]
}

/**
 * Register a style callback function for a named data set
 * @param {string} name name of dataset
 * @param {function} callback style callback function
 */
export function registerStyleFunction (name, callback) {
  styleFunctions[name] = callback
}

/**
 * Predefined catergorical color scales:
 */
export const LABELS = {
  'GAS': {
    'GROEN': {
      label: 'Groen',
      color: 'green'
    },
    'ORANJE': {
      label: 'Oranje',
      color: 'orange'
    }
  },
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
    'WT': {
      label: 'Warmte transport',
      color: 'red'
    },
    'WW': {
      label: 'Warmte wijk',
      color: 'PaleVioletRed '
    },
    'KT': {
      label: 'Koude transport',
      color: 'blue'
    },
    'KW': {
      label: 'Koude wijk',
      color: 'Lightblue'
    }
  },
  'ENERGIE': {
    'A': {
      label: 'A Zeer laag',
      color: 'rgb(14,152,19)'
    },
    'B': {
      label: 'B Laag',
      color: 'rgb(56,223,34)'
    },
    'C': {
      label: 'C Redelijk laag',
      color: 'rgb(180,254,78)'
    },
    'D': {
      label: 'D Gemiddeld',
      color: 'rgb(255,255,53)'
    },
    'E': {
      label: 'E Redelijk hoog',
      color: 'rgb(254,209,78)'
    },
    'F': {
      label: 'F Hoog',
      color: 'rgb(254,130,38)'
    },
    'G': {
      label: 'G Zeer hoog',
      color: 'rgb(223,22,27)'
    }
  }
}

/**
 * For each label counts are kept, this function will reset them all.
 */
export function clearStats () {
  Object.keys(LABELS)
    .map(key => LABELS[key])
    .forEach(label =>
      Object.keys(label).forEach(l => { label[l].count = 0 }))
}

// register style callbacks for various data sets

// Note: the Gas data set is slightly different from the other datasets as it originates
// from two separate data files that were imported as two tables into the database.

/**
 * Get the color for one of the gas datasets:
 * @param {string} id name of the gas data set (either "GROEN" or "ORANJE")
 */
function gasDatasetColor (id) {
  return {
    color: getColor(LABELS.GAS, id)
  }
}

registerStyleFunction('gasgroen', () => gasDatasetColor('GROEN')) // anonymous function as style callback
registerStyleFunction('gasoranje', () => gasDatasetColor('ORANJE'))

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
  const color = getColor(LABELS.WARMTE, feature.properties.selectie)
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
    color: 'gray',
    fill: false,
    weight: 1
  }
}

registerStyleFunction('allborders', allBordersStyle)
