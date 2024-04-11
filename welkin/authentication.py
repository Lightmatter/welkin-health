from __future__ import annotations

import logging
import shelve
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Callable

from portalocker import Lock
from requests.auth import AuthBase

if TYPE_CHECKING:
    from requests import PreparedRequest


logger = logging.getLogger(__name__)


DB_PATH = str(Path(tempfile.gettempdir(), ".welkin.db"))
DB_LOCK = f"{DB_PATH}.lock"


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
        with Lock(DB_LOCK), shelve.open(DB_PATH) as db:  # noqa: S301
            try:
                return db[self.tenant]["token"]
            except KeyError:
                pass

        self.refresh_token()

        return self.token

    @token.setter
    def token(self, value: dict) -> None:
        with Lock(DB_LOCK), shelve.open(DB_PATH) as db:  # noqa: S301
            db[self.tenant] = value

    def refresh_token(self) -> None:
        self.token = self.token_method()
