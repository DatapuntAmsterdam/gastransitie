const OAuth = require('@zalando/oauth2-client-js/dist/oauth2-client')

const CLIENT_ID = 'energietransitie_factsheet'
const SCOPES = ['GAS/R']

// Infer authorization URL
var authzHost = document.location.origin
if (document.location.hostname === 'localhost' ||
  document.location.hostname === '127.0.0.1') {
  authzHost = 'http://' + document.location.hostname + ':8686'
}
const AUTHZ_URL = authzHost + '/oauth2/authorize?idp_id=datapunt'

// Infer redirect_uri
const REDIRECT_URI = document.location.origin + '/'

// provider
const datapuntProvider = new OAuth.Provider({
  id: 'datapunt',
  authorization_url: AUTHZ_URL
})

try {
  datapuntProvider.parse(window.location.hash)
} catch (e) {}

function hasCorrectScopes () {
  var token = datapuntProvider.getAccessToken()
  var payloadB64 = token.split('.')[1]
  var payload = atob(payloadB64 + '='.repeat(payloadB64.length % 4))
  var decoded = JSON.parse(payload)
  if (SCOPES.some(function (e) { return decoded.scopes.indexOf(e) === -1 })) {
    return false
  }
  return true
}

export function authorize () {
  // based on Boris' solution in Citydata
  function stateToken () {
    const crypto = window.crypto || window.msCrypto
    if (!crypto) {
      return '' // empty state is allowed but very much discouraged!
    }
    const list = new Uint8Array(16)
    crypto.getRandomValues(list)
    return btoa(Array
      .from(list) // convert to normal array
      .map((n) => String.fromCharCode(n)) // convert each integer to a character
      .join('')) // convert to a string of characters
  }
  // Create a new request
  var request = new OAuth.Request({
    client_id: CLIENT_ID, // required
    redirect_uri: REDIRECT_URI,
    state: stateToken(),
    scope: SCOPES.join(' ')
  })

  // Give it to the provider
  var uri = datapuntProvider.requestToken(request)

  // Later we need to check if the response was expected
  // so save the request
  datapuntProvider.remember(request)

  // Do the redirect
  window.location.href = uri
}

export function logout () {
  datapuntProvider.deleteTokens()
  window.location.href = REDIRECT_URI
}

export function getToken () {
  if (datapuntProvider.hasAccessToken() && hasCorrectScopes()) {
    return datapuntProvider.getAccessToken()
  }
  return null
}
