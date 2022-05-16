import logging
import shelve
from typing import Callable

from requests import PreparedRequest
from requests.auth import AuthBase

logger = logging.getLogger(__name__)


class WelkinAuth(AuthBase):
    """Attaches API Key Authentication to the given Request object.

    https://developers.welkinhealth.com/#authentication
    """

    def __init__(
        self,
        tenant: str,
        api_client: str,
        secret_key: str,
        token_method: Callable[[], dict],
    ) -> None:
        self.tenant = tenant
        self.api_client = api_client
        self.secret_key = secret_key
        self.token_method = token_method

    def __eq__(self, other: object) -> bool:
        return (self.tenant, self.api_client, self.secret_key) == (
            getattr(other, "tenant", None),
            getattr(other, "api_client", None),
            getattr(other, "secret_key", None),
        )

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        logger.info(f"{r.method} {r.url}")

        if "api_clients" not in r.path_url:
            r.headers["Authorization"] = f"Bearer {self.token}"

        return r

    @property
    def token(self) -> str:
        with shelve.open(".welkin.db") as db:
            try:
                return db[self.tenant]["token"]
            except KeyError:
                pass

        self.refresh_token()

        return self.token

    @token.setter
    def token(self, value: dict) -> None:
        with shelve.open(".welkin.db") as db:
            db[self.tenant] = value

    def refresh_token(self) -> None:
        self.token = self.token_method()
