export function UnknownHostException (message) {
  this.message = message
  this.name = 'uknownHostException'
}

/**
 * Get host appropriate configuratiobn by introspecting document.location.hostname .
 */
export function getConfigForHost () {
  let config = null
  switch (document.location.hostname) {
    case 'localhost':
    case '127.0.0.1':
      config = {
        privateApiHost: 'http://' + document.location.hostname + ':8000',
        authzHost: 'http://' + document.location.hostname + ':8686',
        redirectUri: document.location.origin + '/'
      }
      break
    case 'acc.data.amsterdam.nl':
      config = {
        privateApiHost: 'https://acc.data.amsterdam.nl',
        authzHost: 'https://acc.api.data.amsterdam.nl',
        redirectUri: 'https://acc.data.amsterdam.nl/gastransitie/dash/'
      }
      break
    case 'data.amsterdam.nl':
      config = {
        privateApiHost: 'https://data.amsterdam.nl',
        authzHost: 'https://api.data.amsterdam.nl',
        redirectUri: 'https://data.amsterdam.nl/gastransitie/dash/'
      }
      break
    default:
      let msg = 'Energietransitie frontend running on unknown host, cannot access data.'
      throw new UnknownHostException(msg)
  }
  config.authzUrl = config.authzHost + '/oauth2/authorize?idp_id=datapunt'
  config.privateDataHost = config.privateApiHost // workaround until privateApiHost is phased out

  return config
}
