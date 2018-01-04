/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

window.Authz = function() {
  // config constants
  const CLIENT_ID = 'gastransitie_dashboard'
  const SCOPES = ['GAS/R']

  // Infer authorization URL
  var authzHost = document.location.origin
  if (document.location.hostname == 'localhost' ||
      document.location.hostname == '127.0.0.1') {
      authzHost = 'http://' + document.location.hostname + ':8686'
  }
  const AUTHZ_URL = authzHost + '/oauth2/authorize?idp_id=datapunt'

  // Infer redirect_uri
  const REDIRECT_URI = document.location.origin + '/gastransitie/dash/'

  // imports
  var OAuth = __webpack_require__(1);

  // provider
  const datapuntProvider = new OAuth.Provider({
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

    function authorize() {
      // based on Boris' solution in Citydata
      function stateToken() {
        const crypto = window.crypto || window.msCrypto;
        if (!crypto) {
          return '';  // empty state is allowed but very much discouraged!
        }
        const list = new Uint8Array(16);
        crypto.getRandomValues(list);
        return btoa(Array
          .from(list) // convert to normal array
          .map((n) => String.fromCharCode(n)) // convert each integer to a character
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
      },
    }

  };
}();


/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

/*!
 * Copyright 2015 Zalando SE
 * 
 * Licensed under the Apache License, Version 2.0 (the "License")
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *   http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
(function webpackUniversalModuleDefinition(root, factory) {
	if(true)
		module.exports = factory();
	else if(typeof define === 'function' && define.amd)
		define([], factory);
	else if(typeof exports === 'object')
		exports["oauth2-client-js"] = factory();
	else
		root["oauth2-client-js"] = factory();
})(this, function() {
return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};

/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {

/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;

/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			exports: {},
/******/ 			id: moduleId,
/******/ 			loaded: false
/******/ 		};

/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);

/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;

/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}


/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;

/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;

/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";

/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

	eval("module.exports = __webpack_require__(1);\n\n\n//////////////////\n// WEBPACK FOOTER\n// multi main\n// module id = 0\n// module chunks = 0\n//# sourceURL=webpack:///multi_main?");

/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

	eval("'use strict';\n\nObject.defineProperty(exports, '__esModule', {\n    value: true\n});\n\nfunction _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }\n\nvar _srcProvider = __webpack_require__(2);\n\nvar _srcProvider2 = _interopRequireDefault(_srcProvider);\n\nvar _srcResponse = __webpack_require__(10);\n\nvar _srcResponse2 = _interopRequireDefault(_srcResponse);\n\nvar _srcRequest = __webpack_require__(12);\n\nvar _srcRequest2 = _interopRequireDefault(_srcRequest);\n\nvar _srcError = __webpack_require__(11);\n\nvar _srcError2 = _interopRequireDefault(_srcError);\n\nvar _srcStorageMemoryStorage = __webpack_require__(18);\n\nvar _srcStorageMemoryStorage2 = _interopRequireDefault(_srcStorageMemoryStorage);\n\nexports.Provider = _srcProvider2['default'];\nexports.Response = _srcResponse2['default'];\nexports.Request = _srcRequest2['default'];\nexports.Error = _srcError2['default'];\nexports.MemoryStorage = _srcStorageMemoryStorage2['default'];\n\n//////////////////\n// WEBPACK FOOTER\n// ./oauth.js\n// module id = 1\n// module chunks = 0\n//# sourceURL=webpack:///./oauth.js?");

/***/ }),
/* 2 */
/***/ (function(module, exports, __webpack_require__) {

	eval("'use strict';\n\nObject.defineProperty(exports, '__esModule', {\n    value: true\n});\n\nvar _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ('value' in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();\n\nfunction _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }\n\nfunction _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError('Cannot call a class as a function'); } }\n\nvar _querystring = __webpack_require__(3);\n\nvar _querystring2 = _interopRequireDefault(_querystring);\n\nvar _util = __webpack_require__(6);\n\nvar _storageLocalStorage = __webpack_require__(7);\n\nvar _storageLocalStorage2 = _interopRequireDefault(_storageLocalStorage);\n\nvar _refresh = __webpack_require__(9);\n\nvar _refresh2 = _interopRequireDefault(_refresh);\n\nvar _response = __webpack_require__(10);\n\nvar _response2 = _interopRequireDefault(_response);\n\nvar _error = __webpack_require__(11);\n\nvar _error2 = _interopRequireDefault(_error);\n\nvar Provider = (function () {\n    function Provider(config) {\n        _classCallCheck(this, Provider);\n\n        (0, _util.assertPresent)(config, ['authorization_url', 'id']);\n        this.id = config.id;\n        this.authorization_url = config.authorization_url;\n        this.storage = config.storage || new _storageLocalStorage2['default'](this.id, window.localStorage);\n        this.auth_url_has_query = _util.includes.call(this.authorization_url, '?');\n\n        if (_util.endsWith.call(this.authorization_url, '/') && !this.auth_url_has_query) {\n            this.authorization_url += this.authorization_url.substring(0, this.authorization_url.length - 1);\n        }\n    }\n\n    _createClass(Provider, [{\n        key: 'deleteTokens',\n        value: function deleteTokens() {\n            this.storage.remove('access_token');\n            this.storage.remove('refresh_token');\n        }\n    }, {\n        key: 'remember',\n        value: function remember(request) {\n            if (request.state) {\n                return this.storage.set(request.state, request);\n            }\n            return false;\n        }\n    }, {\n        key: 'forget',\n        value: function forget(request) {\n            return this.storage.remove(request.state);\n        }\n    }, {\n        key: 'isExpected',\n        value: function isExpected(response) {\n            if (response.state) {\n                return !!this.storage.get(response.state);\n            }\n            return false;\n        }\n    }, {\n        key: 'hasAccessToken',\n        value: function hasAccessToken() {\n            return !!this.storage.get('access_token');\n        }\n    }, {\n        key: 'getAccessToken',\n        value: function getAccessToken() {\n            return this.storage.get('access_token');\n        }\n    }, {\n        key: 'setAccessToken',\n        value: function setAccessToken(token) {\n            return this.storage.set('access_token', token);\n        }\n    }, {\n        key: 'hasRefreshToken',\n        value: function hasRefreshToken() {\n            return !!this.storage.get('refresh_token');\n        }\n    }, {\n        key: 'getRefreshToken',\n        value: function getRefreshToken() {\n            return this.storage.get('refresh_token');\n        }\n    }, {\n        key: 'setRefreshToken',\n        value: function setRefreshToken(token) {\n            return this.storage.set('refresh_token', token);\n        }\n    }, {\n        key: 'encodeInUri',\n        value: function encodeInUri(request) {\n            var strippedRequest = (0, _util.stripKeys)(request, ['metadata']);\n            return this.authorization_url + (this.auth_url_has_query ? '&' : '?') + _querystring2['default'].stringify(strippedRequest);\n        }\n    }, {\n        key: 'requestToken',\n        value: function requestToken(request) {\n            return this.encodeInUri(request);\n        }\n    }, {\n        key: 'refreshToken',\n        value: function refreshToken() {\n            return this.hasRefreshToken() ? this.encodeInUri(new _refresh2['default']({ refresh_token: this.getRefreshToken() })) : false;\n        }\n    }, {\n        key: 'decodeFromUri',\n        value: function decodeFromUri(fragment) {\n            var parsed = _querystring2['default'].parse(fragment);\n            return parsed.error ? new _error2['default'](parsed) : new _response2['default'](parsed);\n        }\n    }, {\n        key: 'handleRefresh',\n        value: function handleRefresh(response) {\n            // no state here to check\n            this.setAccessToken(response.access_token);\n            if (response.refresh_token) {\n                this.setRefreshToken(response.refresh_token);\n            }\n        }\n    }, {\n        key: 'handleResponse',\n        value: function handleResponse(response) {\n            if (!this.isExpected(response)) {\n                throw new Error('Unexpected OAuth response', response);\n            }\n            // forget request. seems safe, dunno if replay attacks are possible here in principle\n            var request = this.storage.get(response.state);\n            this.forget(request);\n            response.metadata = request.metadata;\n            if (response instanceof _error2['default']) {\n                return response;\n            }\n            // if we expected this response\n            if (response instanceof _response2['default']) {\n                // update the tokens\n                this.storage._empty();\n                this.setAccessToken(response.access_token);\n                this.setRefreshToken(response.refresh_token);\n                // return the request so that we know\n                return response;\n            }\n            throw new Error('Expected OAuth2 response is neither error nor success. This should not happen.');\n        }\n    }, {\n        key: 'parse',\n        value: function parse(fragment) {\n            if (!fragment) {\n                throw new Error('No URL fragment provided.');\n            }\n            if (typeof fragment !== 'string') {\n                throw new Error('URL fragment is not a string.');\n            }\n            var hash = _util.startsWith.call(fragment, '#') ? fragment.substring(1) : fragment;\n            var response = this.decodeFromUri(hash);\n            return this.handleResponse(response);\n        }\n    }]);\n\n    return Provider;\n})();\n\nexports['default'] = Provider;\nmodule.exports = exports['default'];\n\n//////////////////\n// WEBPACK FOOTER\n// ./src/provider.js\n// module id = 2\n// module chunks = 0\n//# sourceURL=webpack:///./src/provider.js?");

/***/ }),
/* 3 */
/***/ (function(module, exports, __webpack_require__) {

	eval("'use strict';\n\nexports.decode = exports.parse = __webpack_require__(4);\nexports.encode = exports.stringify = __webpack_require__(5);\n\n\n//////////////////\n// WEBPACK FOOTER\n// ./~/querystring/index.js\n// module id = 3\n// module chunks = 0\n//# sourceURL=webpack:///./~/querystring/index.js?");

/***/ }),
/* 4 */
/***/ (function(module, exports) {

	eval("// Copyright Joyent, Inc. and other Node contributors.\n//\n// Permission is hereby granted, free of charge, to any person obtaining a\n// copy of this software and associated documentation files (the\n// \"Software\"), to deal in the Software without restriction, including\n// without limitation the rights to use, copy, modify, merge, publish,\n// distribute, sublicense, and/or sell copies of the Software, and to permit\n// persons to whom the Software is furnished to do so, subject to the\n// following conditions:\n//\n// The above copyright notice and this permission notice shall be included\n// in all copies or substantial portions of the Software.\n//\n// THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS\n// OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF\n// MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN\n// NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,\n// DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR\n// OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE\n// USE OR OTHER DEALINGS IN THE SOFTWARE.\n\n'use strict';\n\n// If obj.hasOwnProperty has been overridden, then calling\n// obj.hasOwnProperty(prop) will break.\n// See: https://github.com/joyent/node/issues/1707\nfunction hasOwnProperty(obj, prop) {\n  return Object.prototype.hasOwnProperty.call(obj, prop);\n}\n\nmodule.exports = function(qs, sep, eq, options) {\n  sep = sep || '&';\n  eq = eq || '=';\n  var obj = {};\n\n  if (typeof qs !== 'string' || qs.length === 0) {\n    return obj;\n  }\n\n  var regexp = /\\+/g;\n  qs = qs.split(sep);\n\n  var maxKeys = 1000;\n  if (options && typeof options.maxKeys === 'number') {\n    maxKeys = options.maxKeys;\n  }\n\n  var len = qs.length;\n  // maxKeys <= 0 means that we should not limit keys count\n  if (maxKeys > 0 && len > maxKeys) {\n    len = maxKeys;\n  }\n\n  for (var i = 0; i < len; ++i) {\n    var x = qs[i].replace(regexp, '%20'),\n        idx = x.indexOf(eq),\n        kstr, vstr, k, v;\n\n    if (idx >= 0) {\n      kstr = x.substr(0, idx);\n      vstr = x.substr(idx + 1);\n    } else {\n      kstr = x;\n      vstr = '';\n    }\n\n    k = decodeURIComponent(kstr);\n    v = decodeURIComponent(vstr);\n\n    if (!hasOwnProperty(obj, k)) {\n      obj[k] = v;\n    } else if (Array.isArray(obj[k])) {\n      obj[k].push(v);\n    } else {\n      obj[k] = [obj[k], v];\n    }\n  }\n\n  return obj;\n};\n\n\n//////////////////\n// WEBPACK FOOTER\n// ./~/querystring/decode.js\n// module id = 4\n// module chunks = 0\n//# sourceURL=webpack:///./~/querystring/decode.js?");

/***/ }),
/* 5 */
/***/ (function(module, exports) {

	eval("// Copyright Joyent, Inc. and other Node contributors.\n//\n// Permission is hereby granted, free of charge, to any person obtaining a\n// copy of this software and associated documentation files (the\n// \"Software\"), to deal in the Software without restriction, including\n// without limitation the rights to use, copy, modify, merge, publish,\n// distribute, sublicense, and/or sell copies of the Software, and to permit\n// persons to whom the Software is furnished to do so, subject to the\n// following conditions:\n//\n// The above copyright notice and this permission notice shall be included\n// in all copies or substantial portions of the Software.\n//\n// THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS\n// OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF\n// MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN\n// NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,\n// DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR\n// OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE\n// USE OR OTHER DEALINGS IN THE SOFTWARE.\n\n'use strict';\n\nvar stringifyPrimitive = function(v) {\n  switch (typeof v) {\n    case 'string':\n      return v;\n\n    case 'boolean':\n      return v ? 'true' : 'false';\n\n    case 'number':\n      return isFinite(v) ? v : '';\n\n    default:\n      return '';\n  }\n};\n\nmodule.exports = function(obj, sep, eq, name) {\n  sep = sep || '&';\n  eq = eq || '=';\n  if (obj === null) {\n    obj = undefined;\n  }\n\n  if (typeof obj === 'object') {\n    return Object.keys(obj).map(function(k) {\n      var ks = encodeURIComponent(stringifyPrimitive(k)) + eq;\n      if (Array.isArray(obj[k])) {\n        return obj[k].map(function(v) {\n          return ks + encodeURIComponent(stringifyPrimitive(v));\n        }).join(sep);\n      } else {\n        return ks + encodeURIComponent(stringifyPrimitive(obj[k]));\n      }\n    }).join(sep);\n\n  }\n\n  if (!name) return '';\n  return encodeURIComponent(stringifyPrimitive(name)) + eq +\n         encodeURIComponent(stringifyPrimitive(obj));\n};\n\n\n//////////////////\n// WEBPACK FOOTER\n// ./~/querystring/encode.js\n// module id = 5\n// module chunks = 0\n//# sourceURL=webpack:///./~/querystring/encode.js?");

/***/ }),
/* 6 */
/***/ (function(module, exports) {

	eval("\"use strict\";\n\nObject.defineProperty(exports, \"__esModule\", {\n    value: true\n});\nfunction assertPresent(obj, fields) {\n    if (obj === undefined) {\n        throw new Error(); //TODO message\n    }\n    fields = fields || [];\n    var undef = fields.filter(function (f) {\n        return obj[f] === undefined;\n    });\n    if (undef.length) {\n        throw new Error(undef[0] + \" is not present on {obj}.\");\n    }\n}\n\nfunction includes(substring) {\n    return this.indexOf(substring) !== -1;\n}\n\nfunction startsWith(substring) {\n    return this.indexOf(substring) === 0;\n}\n\n// https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Global_Objects/String/endsWith\nfunction endsWith(searchString, position) {\n    var subjectString = this.toString();\n    if (position === undefined || position > subjectString.length) {\n        position = subjectString.length;\n    }\n    position -= searchString.length;\n    var lastIndex = subjectString.indexOf(searchString, position);\n    return lastIndex !== -1 && lastIndex === position;\n}\n\nfunction stripKeys(obj, keys) {\n    var stripped = {};\n    keys = keys || [];\n    Object.keys(obj).forEach(function (key) {\n        if (keys.indexOf(key) < 0) {\n            stripped[key] = obj[key];\n        }\n    });\n    return stripped;\n}\n\nexports.assertPresent = assertPresent;\nexports.stripKeys = stripKeys;\nexports.endsWith = endsWith;\nexports.startsWith = startsWith;\nexports.includes = includes;\n\n//////////////////\n// WEBPACK FOOTER\n// ./src/util.js\n// module id = 6\n// module chunks = 0\n//# sourceURL=webpack:///./src/util.js?");

/***/ }),
/* 7 */
/***/ (function(module, exports, __webpack_require__) {

	eval("'use strict';\n\nObject.defineProperty(exports, '__esModule', {\n    value: true\n});\n\nvar _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ('value' in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();\n\nvar _get = function get(_x, _x2, _x3) { var _again = true; _function: while (_again) { var object = _x, property = _x2, receiver = _x3; _again = false; if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { _x = parent; _x2 = property; _x3 = receiver; _again = true; desc = parent = undefined; continue _function; } } else if ('value' in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } } };\n\nfunction _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }\n\nfunction _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError('Cannot call a class as a function'); } }\n\nfunction _inherits(subClass, superClass) { if (typeof superClass !== 'function' && superClass !== null) { throw new TypeError('Super expression must either be null or a function, not ' + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }\n\nvar _storage = __webpack_require__(8);\n\nvar _storage2 = _interopRequireDefault(_storage);\n\nvar _util = __webpack_require__(6);\n\nvar LocalTokenStorage = (function (_OAuthTokenStorage) {\n    _inherits(LocalTokenStorage, _OAuthTokenStorage);\n\n    function LocalTokenStorage(prefix, localStorage) {\n        _classCallCheck(this, LocalTokenStorage);\n\n        _get(Object.getPrototypeOf(LocalTokenStorage.prototype), 'constructor', this).call(this);\n        (0, _util.assertPresent)(prefix);\n        (0, _util.assertPresent)(localStorage);\n        this.localStorage = localStorage;\n        this.prefix = prefix;\n    }\n\n    _createClass(LocalTokenStorage, [{\n        key: 'get',\n        value: function get(key) {\n            var item = this.localStorage.getItem(this.prefix + '-' + key);\n            try {\n                item = JSON.parse(item);\n            } catch (err) {\n                return item;\n            }\n            return item;\n        }\n    }, {\n        key: 'set',\n        value: function set(key, val) {\n            var toSave = typeof val === 'object' ? JSON.stringify(val) : val;\n            return this.localStorage.setItem(this.prefix + '-' + key, toSave);\n        }\n    }, {\n        key: 'remove',\n        value: function remove(key) {\n            return this.localStorage.removeItem(this.prefix + '-' + key);\n        }\n    }, {\n        key: '_empty',\n        value: function _empty() {\n            var _this = this;\n\n            Object.keys(this.localStorage).forEach(function (key) {\n                if (key.startsWith(_this.prefix)) {\n                    _this.localStorage.removeItem(key);\n                }\n            });\n        }\n\n        // do *NOT* call this outside of tests\n    }, {\n        key: '_purge',\n        value: function _purge() {\n            this.localStorage.clear();\n        }\n    }]);\n\n    return LocalTokenStorage;\n})(_storage2['default']);\n\nexports['default'] = LocalTokenStorage;\nmodule.exports = exports['default'];\n\n//////////////////\n// WEBPACK FOOTER\n// ./src/storage/local-storage.js\n// module id = 7\n// module chunks = 0\n//# sourceURL=webpack:///./src/storage/local-storage.js?");

/***/ }),
/* 8 */
/***/ (function(module, exports) {

	eval("\"use strict\";\n\nObject.defineProperty(exports, \"__esModule\", {\n    value: true\n});\n\nvar _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if (\"value\" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();\n\nfunction _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError(\"Cannot call a class as a function\"); } }\n\nvar OAuthTokenStorage = (function () {\n    function OAuthTokenStorage() {\n        _classCallCheck(this, OAuthTokenStorage);\n    }\n\n    /* eslint-disable */\n\n    _createClass(OAuthTokenStorage, [{\n        key: \"get\",\n        value: function get(key) {}\n    }, {\n        key: \"set\",\n        value: function set(key, val) {}\n    }, {\n        key: \"remove\",\n        value: function remove(key) {}\n    }, {\n        key: \"_empty\",\n        value: function _empty() {}\n    }, {\n        key: \"_purge\",\n        value: function _purge() {}\n\n        /* eslint-enable */\n    }]);\n\n    return OAuthTokenStorage;\n})();\n\nexports[\"default\"] = OAuthTokenStorage;\nmodule.exports = exports[\"default\"];\n\n//////////////////\n// WEBPACK FOOTER\n// ./src/storage/storage.js\n// module id = 8\n// module chunks = 0\n//# sourceURL=webpack:///./src/storage/storage.js?");

/***/ }),
/* 9 */
/***/ (function(module, exports, __webpack_require__) {

	eval("'use strict';\n\nObject.defineProperty(exports, '__esModule', {\n    value: true\n});\n\nfunction _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError('Cannot call a class as a function'); } }\n\nvar _util = __webpack_require__(6);\n\nvar RefreshRequest = function RefreshRequest(config) {\n    _classCallCheck(this, RefreshRequest);\n\n    (0, _util.assertPresent)(config, ['refresh_token']);\n    this.grant_type = 'refresh_token';\n    this.refresh_token = config.refresh_token;\n    this.scope = config.scope;\n};\n\nexports['default'] = RefreshRequest;\nmodule.exports = exports['default'];\n\n//////////////////\n// WEBPACK FOOTER\n// ./src/refresh.js\n// module id = 9\n// module chunks = 0\n//# sourceURL=webpack:///./src/refresh.js?");

/***/ }),
/* 10 */
/***/ (function(module, exports, __webpack_require__) {

	eval("'use strict';\n\nObject.defineProperty(exports, '__esModule', {\n    value: true\n});\n\nvar _get = function get(_x, _x2, _x3) { var _again = true; _function: while (_again) { var object = _x, property = _x2, receiver = _x3; _again = false; if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { _x = parent; _x2 = property; _x3 = receiver; _again = true; desc = parent = undefined; continue _function; } } else if ('value' in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } } };\n\nfunction _inherits(subClass, superClass) { if (typeof superClass !== 'function' && superClass !== null) { throw new TypeError('Super expression must either be null or a function, not ' + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }\n\nfunction _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError('Cannot call a class as a function'); } }\n\nvar _util = __webpack_require__(6);\n\n/**\n * As per RFC 6749\n * ---\n * - access_token: REQUIRED\n * - token_type: REQUIRED\n * - expires_in: RECOMMENDED\n * - scope: OPTIONAL\n * - refresh_token: OPTIONAL\n */\n\nvar OAuthResponse = function OAuthResponse(response) {\n    _classCallCheck(this, OAuthResponse);\n\n    this.response = response;\n    (0, _util.assertPresent)(response, ['access_token', 'token_type']);\n\n    this.access_token = response.access_token;\n    this.token_type = response.token_type;\n    this.refresh_token = response.refresh_token || null;\n    this.expires_in = response.expires_in ? parseInt(response.expires_in) : null;\n    this.scope = response.scope;\n};\n\nvar OAuthImplicitResponse = (function (_OAuthResponse) {\n    _inherits(OAuthImplicitResponse, _OAuthResponse);\n\n    function OAuthImplicitResponse(response) {\n        _classCallCheck(this, OAuthImplicitResponse);\n\n        _get(Object.getPrototypeOf(OAuthImplicitResponse.prototype), 'constructor', this).call(this, response);\n        (0, _util.assertPresent)(response, ['state']);\n        this.state = response.state;\n    }\n\n    return OAuthImplicitResponse;\n})(OAuthResponse);\n\nexports.Response = OAuthResponse;\nexports['default'] = OAuthImplicitResponse;\n\n//////////////////\n// WEBPACK FOOTER\n// ./src/response.js\n// module id = 10\n// module chunks = 0\n//# sourceURL=webpack:///./src/response.js?");

/***/ }),
/* 11 */
/***/ (function(module, exports, __webpack_require__) {

	eval("'use strict';\n\nObject.defineProperty(exports, '__esModule', {\n    value: true\n});\n\nvar _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ('value' in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();\n\nfunction _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError('Cannot call a class as a function'); } }\n\nvar _util = __webpack_require__(6);\n\nvar OAuthErrorResponse = (function () {\n    function OAuthErrorResponse(response) {\n        _classCallCheck(this, OAuthErrorResponse);\n\n        (0, _util.assertPresent)(response, ['error', 'state']);\n        //TODO maybe check valid errors\n        this.error = response.error;\n        this.state = response.state;\n        this.error_description = response.error_description;\n    }\n\n    _createClass(OAuthErrorResponse, [{\n        key: 'getMessage',\n        value: function getMessage() {\n            //TODO RFC 6749 Section 4.2.2.1\n            return this.error_description;\n        }\n    }]);\n\n    return OAuthErrorResponse;\n})();\n\nexports['default'] = OAuthErrorResponse;\nmodule.exports = exports['default'];\n\n//////////////////\n// WEBPACK FOOTER\n// ./src/error.js\n// module id = 11\n// module chunks = 0\n//# sourceURL=webpack:///./src/error.js?");

/***/ }),
/* 12 */
/***/ (function(module, exports, __webpack_require__) {

	eval("'use strict';\n\nObject.defineProperty(exports, '__esModule', {\n    value: true\n});\n\nvar _get = function get(_x, _x2, _x3) { var _again = true; _function: while (_again) { var object = _x, property = _x2, receiver = _x3; _again = false; if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { _x = parent; _x2 = property; _x3 = receiver; _again = true; desc = parent = undefined; continue _function; } } else if ('value' in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } } };\n\nfunction _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }\n\nfunction _inherits(subClass, superClass) { if (typeof superClass !== 'function' && superClass !== null) { throw new TypeError('Super expression must either be null or a function, not ' + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }\n\nfunction _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError('Cannot call a class as a function'); } }\n\nvar _util = __webpack_require__(6);\n\nvar _uuid = __webpack_require__(13);\n\nvar _uuid2 = _interopRequireDefault(_uuid);\n\n/**\n * As per RFC 6749, Section 4.2.1\n * ----\n * - response_type: REQUIRED, MUST be \"token\"\n * - client_id: REQUIRED\n * - redirect_uri: OPTIONAL\n * - scope: OPTIONAL\n * - state: RECOMMENDED\n */\n\nvar OAuthRequest = function OAuthRequest(config) {\n    _classCallCheck(this, OAuthRequest);\n\n    (0, _util.assertPresent)(config, ['response_type']);\n\n    this.response_type = config.response_type;\n    this.scope = config.scope;\n    this.metadata = config.metadata || {};\n};\n\nvar OAuthImplicitRequest = (function (_OAuthRequest) {\n    _inherits(OAuthImplicitRequest, _OAuthRequest);\n\n    function OAuthImplicitRequest(config) {\n        _classCallCheck(this, OAuthImplicitRequest);\n\n        config.response_type = 'token';\n        _get(Object.getPrototypeOf(OAuthImplicitRequest.prototype), 'constructor', this).call(this, config);\n        (0, _util.assertPresent)(config, ['client_id']);\n        this.client_id = config.client_id;\n        this.redirect_uri = config.redirect_uri;\n        this.state = config.state !== undefined ? config.state : _uuid2['default'].v4();\n    }\n\n    return OAuthImplicitRequest;\n})(OAuthRequest);\n\nexports['default'] = OAuthImplicitRequest;\nmodule.exports = exports['default'];\n\n//////////////////\n// WEBPACK FOOTER\n// ./src/request.js\n// module id = 12\n// module chunks = 0\n//# sourceURL=webpack:///./src/request.js?");

/***/ }),
/* 13 */
/***/ (function(module, exports, __webpack_require__) {

	eval("var v1 = __webpack_require__(14);\nvar v4 = __webpack_require__(17);\n\nvar uuid = v4;\nuuid.v1 = v1;\nuuid.v4 = v4;\n\nmodule.exports = uuid;\n\n\n//////////////////\n// WEBPACK FOOTER\n// ./~/uuid/index.js\n// module id = 13\n// module chunks = 0\n//# sourceURL=webpack:///./~/uuid/index.js?");

/***/ }),
/* 14 */
/***/ (function(module, exports, __webpack_require__) {

	eval("var rng = __webpack_require__(15);\nvar bytesToUuid = __webpack_require__(16);\n\n// **`v1()` - Generate time-based UUID**\n//\n// Inspired by https://github.com/LiosK/UUID.js\n// and http://docs.python.org/library/uuid.html\n\n// random #'s we need to init node and clockseq\nvar _seedBytes = rng();\n\n// Per 4.5, create and 48-bit node id, (47 random bits + multicast bit = 1)\nvar _nodeId = [\n  _seedBytes[0] | 0x01,\n  _seedBytes[1], _seedBytes[2], _seedBytes[3], _seedBytes[4], _seedBytes[5]\n];\n\n// Per 4.2.2, randomize (14 bit) clockseq\nvar _clockseq = (_seedBytes[6] << 8 | _seedBytes[7]) & 0x3fff;\n\n// Previous uuid creation time\nvar _lastMSecs = 0, _lastNSecs = 0;\n\n// See https://github.com/broofa/node-uuid for API details\nfunction v1(options, buf, offset) {\n  var i = buf && offset || 0;\n  var b = buf || [];\n\n  options = options || {};\n\n  var clockseq = options.clockseq !== undefined ? options.clockseq : _clockseq;\n\n  // UUID timestamps are 100 nano-second units since the Gregorian epoch,\n  // (1582-10-15 00:00).  JSNumbers aren't precise enough for this, so\n  // time is handled internally as 'msecs' (integer milliseconds) and 'nsecs'\n  // (100-nanoseconds offset from msecs) since unix epoch, 1970-01-01 00:00.\n  var msecs = options.msecs !== undefined ? options.msecs : new Date().getTime();\n\n  // Per 4.2.1.2, use count of uuid's generated during the current clock\n  // cycle to simulate higher resolution clock\n  var nsecs = options.nsecs !== undefined ? options.nsecs : _lastNSecs + 1;\n\n  // Time since last uuid creation (in msecs)\n  var dt = (msecs - _lastMSecs) + (nsecs - _lastNSecs)/10000;\n\n  // Per 4.2.1.2, Bump clockseq on clock regression\n  if (dt < 0 && options.clockseq === undefined) {\n    clockseq = clockseq + 1 & 0x3fff;\n  }\n\n  // Reset nsecs if clock regresses (new clockseq) or we've moved onto a new\n  // time interval\n  if ((dt < 0 || msecs > _lastMSecs) && options.nsecs === undefined) {\n    nsecs = 0;\n  }\n\n  // Per 4.2.1.2 Throw error if too many uuids are requested\n  if (nsecs >= 10000) {\n    throw new Error('uuid.v1(): Can\\'t create more than 10M uuids/sec');\n  }\n\n  _lastMSecs = msecs;\n  _lastNSecs = nsecs;\n  _clockseq = clockseq;\n\n  // Per 4.1.4 - Convert from unix epoch to Gregorian epoch\n  msecs += 12219292800000;\n\n  // `time_low`\n  var tl = ((msecs & 0xfffffff) * 10000 + nsecs) % 0x100000000;\n  b[i++] = tl >>> 24 & 0xff;\n  b[i++] = tl >>> 16 & 0xff;\n  b[i++] = tl >>> 8 & 0xff;\n  b[i++] = tl & 0xff;\n\n  // `time_mid`\n  var tmh = (msecs / 0x100000000 * 10000) & 0xfffffff;\n  b[i++] = tmh >>> 8 & 0xff;\n  b[i++] = tmh & 0xff;\n\n  // `time_high_and_version`\n  b[i++] = tmh >>> 24 & 0xf | 0x10; // include version\n  b[i++] = tmh >>> 16 & 0xff;\n\n  // `clock_seq_hi_and_reserved` (Per 4.2.2 - include variant)\n  b[i++] = clockseq >>> 8 | 0x80;\n\n  // `clock_seq_low`\n  b[i++] = clockseq & 0xff;\n\n  // `node`\n  var node = options.node || _nodeId;\n  for (var n = 0; n < 6; ++n) {\n    b[i + n] = node[n];\n  }\n\n  return buf ? buf : bytesToUuid(b);\n}\n\nmodule.exports = v1;\n\n\n//////////////////\n// WEBPACK FOOTER\n// ./~/uuid/v1.js\n// module id = 14\n// module chunks = 0\n//# sourceURL=webpack:///./~/uuid/v1.js?");

/***/ }),
/* 15 */
/***/ (function(module, exports) {

	eval("/* WEBPACK VAR INJECTION */(function(global) {// Unique ID creation requires a high quality random # generator.  In the\n// browser this is a little complicated due to unknown quality of Math.random()\n// and inconsistent support for the `crypto` API.  We do the best we can via\n// feature-detection\nvar rng;\n\nvar crypto = global.crypto || global.msCrypto; // for IE 11\nif (crypto && crypto.getRandomValues) {\n  // WHATWG crypto RNG - http://wiki.whatwg.org/wiki/Crypto\n  var rnds8 = new Uint8Array(16); // eslint-disable-line no-undef\n  rng = function whatwgRNG() {\n    crypto.getRandomValues(rnds8);\n    return rnds8;\n  };\n}\n\nif (!rng) {\n  // Math.random()-based (RNG)\n  //\n  // If all else fails, use Math.random().  It's fast, but is of unspecified\n  // quality.\n  var rnds = new Array(16);\n  rng = function() {\n    for (var i = 0, r; i < 16; i++) {\n      if ((i & 0x03) === 0) r = Math.random() * 0x100000000;\n      rnds[i] = r >>> ((i & 0x03) << 3) & 0xff;\n    }\n\n    return rnds;\n  };\n}\n\nmodule.exports = rng;\n\n/* WEBPACK VAR INJECTION */}.call(exports, (function() { return this; }())))\n\n//////////////////\n// WEBPACK FOOTER\n// ./~/uuid/lib/rng-browser.js\n// module id = 15\n// module chunks = 0\n//# sourceURL=webpack:///./~/uuid/lib/rng-browser.js?");

/***/ }),
/* 16 */
/***/ (function(module, exports) {

	eval("/**\n * Convert array of 16 byte values to UUID string format of the form:\n * XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX\n */\nvar byteToHex = [];\nfor (var i = 0; i < 256; ++i) {\n  byteToHex[i] = (i + 0x100).toString(16).substr(1);\n}\n\nfunction bytesToUuid(buf, offset) {\n  var i = offset || 0;\n  var bth = byteToHex;\n  return bth[buf[i++]] + bth[buf[i++]] +\n          bth[buf[i++]] + bth[buf[i++]] + '-' +\n          bth[buf[i++]] + bth[buf[i++]] + '-' +\n          bth[buf[i++]] + bth[buf[i++]] + '-' +\n          bth[buf[i++]] + bth[buf[i++]] + '-' +\n          bth[buf[i++]] + bth[buf[i++]] +\n          bth[buf[i++]] + bth[buf[i++]] +\n          bth[buf[i++]] + bth[buf[i++]];\n}\n\nmodule.exports = bytesToUuid;\n\n\n//////////////////\n// WEBPACK FOOTER\n// ./~/uuid/lib/bytesToUuid.js\n// module id = 16\n// module chunks = 0\n//# sourceURL=webpack:///./~/uuid/lib/bytesToUuid.js?");

/***/ }),
/* 17 */
/***/ (function(module, exports, __webpack_require__) {

	eval("var rng = __webpack_require__(15);\nvar bytesToUuid = __webpack_require__(16);\n\nfunction v4(options, buf, offset) {\n  var i = buf && offset || 0;\n\n  if (typeof(options) == 'string') {\n    buf = options == 'binary' ? new Array(16) : null;\n    options = null;\n  }\n  options = options || {};\n\n  var rnds = options.random || (options.rng || rng)();\n\n  // Per 4.4, set bits for version and `clock_seq_hi_and_reserved`\n  rnds[6] = (rnds[6] & 0x0f) | 0x40;\n  rnds[8] = (rnds[8] & 0x3f) | 0x80;\n\n  // Copy bytes to buffer, if provided\n  if (buf) {\n    for (var ii = 0; ii < 16; ++ii) {\n      buf[i + ii] = rnds[ii];\n    }\n  }\n\n  return buf || bytesToUuid(rnds);\n}\n\nmodule.exports = v4;\n\n\n//////////////////\n// WEBPACK FOOTER\n// ./~/uuid/v4.js\n// module id = 17\n// module chunks = 0\n//# sourceURL=webpack:///./~/uuid/v4.js?");

/***/ }),
/* 18 */
/***/ (function(module, exports, __webpack_require__) {

	eval("'use strict';\n\nObject.defineProperty(exports, '__esModule', {\n    value: true\n});\n\nvar _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ('value' in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();\n\nvar _get = function get(_x, _x2, _x3) { var _again = true; _function: while (_again) { var object = _x, property = _x2, receiver = _x3; _again = false; if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { _x = parent; _x2 = property; _x3 = receiver; _again = true; desc = parent = undefined; continue _function; } } else if ('value' in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } } };\n\nfunction _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }\n\nfunction _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError('Cannot call a class as a function'); } }\n\nfunction _inherits(subClass, superClass) { if (typeof superClass !== 'function' && superClass !== null) { throw new TypeError('Super expression must either be null or a function, not ' + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }\n\nvar _storage = __webpack_require__(8);\n\nvar _storage2 = _interopRequireDefault(_storage);\n\nvar MemoryTokenStorage = (function (_OAuthTokenStorage) {\n    _inherits(MemoryTokenStorage, _OAuthTokenStorage);\n\n    function MemoryTokenStorage() {\n        _classCallCheck(this, MemoryTokenStorage);\n\n        _get(Object.getPrototypeOf(MemoryTokenStorage.prototype), 'constructor', this).call(this);\n        this.items = {};\n    }\n\n    _createClass(MemoryTokenStorage, [{\n        key: 'get',\n        value: function get(key) {\n            return this.items[key];\n        }\n    }, {\n        key: 'set',\n        value: function set(key, val) {\n            this.items[key] = val;\n            return this.get(key);\n        }\n    }, {\n        key: 'remove',\n        value: function remove(key) {\n            delete this.items[key];\n        }\n    }, {\n        key: '_empty',\n        value: function _empty() {\n            this.items = {};\n        }\n    }, {\n        key: '_purge',\n        value: function _purge() {\n            this.items = {};\n        }\n    }]);\n\n    return MemoryTokenStorage;\n})(_storage2['default']);\n\nexports['default'] = MemoryTokenStorage;\nmodule.exports = exports['default'];\n\n//////////////////\n// WEBPACK FOOTER\n// ./src/storage/memory-storage.js\n// module id = 18\n// module chunks = 0\n//# sourceURL=webpack:///./src/storage/memory-storage.js?");

/***/ })
/******/ ])
});
;

/***/ })
/******/ ]);