window.Authz = function() {
  // config constants
  var CLIENT_ID = 'gastransitie_dashboard'
  var SCOPES = ['GAS/R']

  // Infer authorization URL
  var authzHost = document.location.origin
  if (document.location.hostname == 'localhost' ||
      document.location.hostname == '127.0.0.1') {
      authzHost = 'http://' + document.location.hostname + ':8686'
  }
  var AUTHZ_URL = authzHost + '/oauth2/authorize?idp_id=datapunt'

  // Infer redirect_uri
  var REDIRECT_URI = document.location.origin + '/gastransitie/dash/'

  // imports
  var OAuth = __webpack_require__(1);

  // provider
  var datapuntProvider = new OAuth.Provider({
      id: 'datapunt',
      authorization_url: AUTHZ_URL
  })

  try {
    datapuntProvider.parse(window.location.hash)
  } catch(e) {}

  return function(elmID) {

    function hasCorrectScopes() {
      var token = datapuntProvider.getAccessToken();
      var payloadB64 = token.split('.')[1];
      var payload = atob(payloadB64 + '='.repeat(payloadB64.length % 4));
      var decoded = JSON.parse(payload);
      if (SCOPES.some(function(e) { return decoded.scopes.indexOf(e) == -1 })) {
        return false
      }
      return true
    }

    function convertIntToChar(n) {
        return String.fromCharCode(n)
    }

    function authorize() {
      // based on Boris' solution in Citydata
      function stateToken() {
        var crypto = window.crypto || window.msCrypto;
        if (!crypto) {
          return '';  // empty state is allowed but very much discouraged!
        }
        var list = new Uint8Array(16);
        crypto.getRandomValues(list);
        return btoa(Array
          .from(list) // convert to normal array
          .map(convertIntToChar) // convert each integer to a character
          .join('')); // convert to a string of characters
      }
      // Create a new request
      var request = new OAuth.Request({
        client_id: CLIENT_ID,  // required
        redirect_uri: REDIRECT_URI,
        state: stateToken(),
        scope: SCOPES.join(' ')
      });

      // Give it to the provider
      var uri = datapuntProvider.requestToken(request);

      // Later we need to check if the response was expected
      // so save the request
      datapuntProvider.remember(request);

      // Do the redirect
      window.location.href = uri;
    }

    return {
      token: function() {
        if (datapuntProvider.hasAccessToken() && hasCorrectScopes()) {
          return datapuntProvider.getAccessToken();
        }
        return null
      },
      askLogin: function() {
        var msgcontainer = document.getElementById(elmID);
        var loginButton = document.createElement('button');
        loginButton.onclick = authorize;
        loginButton.innerHTML = 'Inloggen';
        if (!datapuntProvider.hasAccessToken()) {
          msgcontainer.appendChild(document.createTextNode("U bent niet ingelogd."));
        } else if (!hasCorrectScopes()) {
          datapuntProvider.deleteTokens();
          msgcontainer.appendChild(document.createTextNode("U heeft niet voldoende rechten. U kunt inloggen als een andere gebruiker."));
        } else {
          datapuntProvider.deleteTokens();
          msgcontainer.appendChild(document.createTextNode("U bent niet meer ingelogd."));
        }
        msgcontainer.appendChild(loginButton);
      }
    }

  };
}();
