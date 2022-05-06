import logging
import shelve

import requests
from requests import HTTPError
from requests.auth import HTTPBasicAuth

from welkin.exceptions import WelkinHTTPError

logger = logging.getLogger(__name__)


class WelkinAuth(HTTPBasicAuth):
    """Attaches API Key Authentication to the given Request object.

    https://developers.welkinhealth.com/#authentication
    """

    def __init__(self, tenant, api_client, secret_key, token_method):
        self.tenant = tenant
        self.api_client = api_client
        self.secret_key = secret_key
        self.token_method = token_method

    def __eq__(self, other):
        return (self.tenant, self.api_client, self.secret_key) == (
            other.tenant,
            other.api_client,
            other.secret_key,
        )

    def __call__(self, r):
        logger.info(f"{r.method} {r.url}")

        if "api_clients" not in r.path_url:
            r.headers["Authorization"] = f"Bearer {self.token}"

        return r

    @property
    def token(self):
        with shelve.open("welkin") as db:
            try:
                return db[self.tenant]["token"]
            except KeyError:
                self.refresh_token()
                return self.token

    @token.setter
    def token(self, value):
        with shelve.open("welkin") as db:
            db[self.tenant] = value

    def refresh_token(self):
        self.token = self.token_method()
