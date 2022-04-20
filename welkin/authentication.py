import logging
import shelve
from functools import cached_property

import requests
from requests import HTTPError
from requests.auth import HTTPBasicAuth

from welkin.exceptions import WelkinHTTPError

logger = logging.getLogger(__name__)


class WelkinAuth(HTTPBasicAuth):
    """Attaches API Key Authentication to the given Request object."""

    def __init__(self, tenant, api_client, secret_key):
        self.tenant = tenant
        self.api_client = api_client
        self.secret_key = secret_key

        self.token = self.obtain_token()

    def __eq__(self, other):
        return (self.tenant, self.api_client, self.secret_key) == (
            other.tenant,
            other.api_client,
            other.secret_key,
        )

    def __call__(self, r):
        logger.info(f"{r.method} {r.url}")
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r

    def obtain_token(self):
        with shelve.open("welkin") as db:
            try:
                return db[self.tenant]["token"]
            except KeyError:
                pass

            response = requests.post(
                f"https://api.live.welkincloud.io/{self.tenant}/admin/api_clients/{self.api_client}",
                json={"secret": self.secret_key},
            )
            try:
                response.raise_for_status()
            except HTTPError as exc:
                raise WelkinHTTPError(exc.request, exc.response) from exc

            db[self.tenant] = response.json()

            return db[self.tenant]["token"]
