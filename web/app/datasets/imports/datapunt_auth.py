"""
Download per buurt alle vestigingen van dataselectie.
"""
import time
import jwt
import logging
import os

import authorization_levels
from authorization_django import jwks

log = logging.getLogger(__name__)


class AuthorizationSetup(object):
    """
    Helper methods to setup JWT tokens and authorization levels

    sets the following attributes:

    token_default
    token_employee
    token_employee_plus
    """
    def __init__(self):

        self.token_default = None
        self.token_employee = None
        self.token_employee_plus = None

        self.set_up_authorization()

    def set_up_authorization(self):
        """
        SET

        token_default
        token_employee
        token_employee_plus

        to use with:

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer {}'.format(self.token_employee_plus))

        """
        # NEW STYLE AUTH
        # The following JWKS data was obtained in the authz project :  jwkgen -create -alg ES256    # noqa
        # This is a test public/private key def and added for testing .
        JWKS_TEST_KEY = """
            {
                "keys": [
                    {
                        "kty": "EC",
                        "key_ops": [
                            "verify",
                            "sign"
                        ],
                        "kid": "2aedafba-8170-4064-b704-ce92b7c89cc6",
                        "crv": "P-256",
                        "x": "6r8PYwqfZbq_QzoMA4tzJJsYUIIXdeyPA27qTgEJCDw=",
                        "y": "Cf2clfAfFuuCB06NMfIat9ultkMyrMQO9Hd2H7O9ZVE=",
                        "d": "N1vu0UQUp0vLfaNeM0EDbl4quvvL6m_ltjoAXXzkI3U="
                    }
                ]
            }
        """

        jwks_string = os.getenv('PUB_JWKS', JWKS_TEST_KEY)
        jwks_signers = jwks.load(jwks_string).signers

        assert len(jwks_signers) > 0

        if len(jwks_signers) == 0:
            print("""

            WARNING WARNING WARNING

            'JWT_SECRET_KEY' MISSING!!

            """)
            return False

        list_signers = [(k, v) for k, v in jwks_signers.items()]
        (kid, key) = list_signers[len(list_signers)-1]
        header = {"kid": kid}

        log.info('We can create authorized requests!')

        now = int(time.time())

        valid_seconds = 7200

        token_default = jwt.encode({
            'scopes': [],
            'iat': now, 'exp': now + valid_seconds},
            key.key, algorithm=key.alg, headers=header)
        token_employee = jwt.encode({
            'scopes': [s for s in authorization_levels.SCOPES_EMPLOYEE],
            'iat': now, 'exp': now + valid_seconds},
            key.key, algorithm=key.alg, headers=header)
        token_employee_plus = jwt.encode({
            'scopes': [s for s in authorization_levels.SCOPES_EMPLOYEE_PLUS],
            'iat': now, 'exp': now + valid_seconds},
            key.key, algorithm=key.alg, headers=header)

        self.token_default = str(token_default, 'utf-8')
        self.token_employee = str(token_employee, 'utf-8')
        self.token_employee_plus = str(token_employee_plus, 'utf-8')


auth = AuthorizationSetup()
