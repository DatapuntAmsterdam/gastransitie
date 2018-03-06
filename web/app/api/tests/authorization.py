import time
import jwt

from authorization_django.config import settings as middleware_settings


class AuthorizationSetup(object):
    """
    Helper methods to setup JWT tokens and authorization levels

    sets the following attributes:

    token_scope_hr
    """

    def setUpAuthorization(self):
        """
        SET

        token_scope_hr

        to use with:

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer {}'.format(self.token_scope_hr))

        """
        # VERY NEW STYLE AUTH. JWKS public/private keys are defined in settings
        jwks = middleware_settings()['JWKS'].signers

        assert len(jwks) > 0
        (kid, key), = jwks.items()

        now = int(time.time())

        token_scope_gas = jwt.encode({
            'scopes': ['GAS/R'],
            'iat': now, 'exp': now + 600}, key.key, algorithm=key.alg,
             headers={'kid': kid})

        self.token_scope_gas = str(token_scope_gas, 'utf-8')
