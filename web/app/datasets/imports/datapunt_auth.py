"""
Download per buurt alle vestigingen van dataselectie.
"""
import requests
import os
import random
import string

from urllib.parse import urlparse, parse_qsl

import time
import jwt
import logging
import os

import authorization_levels
from authorization_django import jwks

log = logging.getLogger(__name__)

# utf-8


class GetAccessToken(object):
    """
        Get an header authentication item for access token
        for using the internal API's
        by logging in as type = 'employee'

        Usage:
            from accesstoken import AccessToken
            getToken = AccessToken()
            accessToken = getToken.getAccessToken()
            requests.get(url, headers= accessToken)
    """
    def get_auth_header(self):
        email = os.getenv('GAS_USER', 'gastransitie_api_user')
        password = os.getenv('GAS_API_PASSWORD')   # crash hard when missing.
        acceptance = os.getenv('ENVIRONMENT', 'acceptance') == 'acceptance'
        access_token = GetAccessToken().getAccessToken(
            email, password, acceptance)
        return access_token

    def getAccessToken(self, email, password, acceptance):

        def randomword(length):
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(length))

        state = randomword(10)
        # scopes = ['SIG/ALL']
        scopes = ['HR/R', 'BRK/RSN', 'BRK/RS']
        acc_prefix = 'acc.' if acceptance else ''
        authzUrl = f'https://{acc_prefix}api.data.amsterdam.nl/oauth2/authorize'   # noqa
        params = {
            'idp_id': 'datapunt',
            'response_type': 'token',
            'client_id': 'citydata',
            'scope': ' '.join(scopes),
            'state': state,
            'redirect_uri': f'https://{acc_prefix}data.amsterdam.nl/'
        }

        response = requests.get(authzUrl, params, allow_redirects=False)
        if response.status_code == 303:
            location = response.headers["Location"]
        else:
            return {}

        data = {
            'type': 'employee_plus',
            'email': email,
            'password': password,
        }

        response = requests.post(location, data=data, allow_redirects=False)
        if response.status_code == 303:
            location = response.headers["Location"]
        else:
            return {}

        response = requests.get(location, allow_redirects=False)
        if response.status_code == 303:
            returnedUrl = response.headers["Location"]
        else:
            return {}

        # Get grantToken from parameter aselect_credentials in session URL
        parsed = urlparse(returnedUrl)
        fragment = parse_qsl(parsed.fragment)
        access_token = fragment[0][1]
        os.environ["ACCESS_TOKEN"] = access_token
        return {"Authorization": 'Bearer ' + access_token}


if __name__ == "__main__":
    acceptance = True
    email = os.getenv('GAS_USER', 'gastransitie_api_user')
    password = os.getenv('GAS_API_PASSWORD')    # crash hard when missing.
    access_token = GetAccessToken().getAccessToken(
        email, password, acceptance)
    print(f'Received new Access Token Header: {access_token}')
    url = "https://acc.api.data.amsterdam.nl/dataselectie/hr/export/?buurt_naam=Aalsmeerwegbuurt+Oost"   # noqa
    # url = "https://acc.api.data.amsterdam.nl/brk/subject/?buurt=K44d&zakelijk_recht=2"  # noqa
    response = requests.get(url, headers=access_token)
    csvresponse = response.text
    print(csvresponse)
