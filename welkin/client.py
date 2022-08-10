"""Client

This module provides a Client object to interface with the Welkin Health API.
"""
import logging
from json import JSONDecodeError

from requests import HTTPError, Session
from requests.adapters import HTTPAdapter
from requests.compat import urljoin
from requests.packages.urllib3.util.retry import Retry  # type: ignore

from welkin import __version__
from welkin.authentication import WelkinAuth
from welkin.exceptions import WelkinHTTPError
from welkin.models import *
from welkin.util import clean_request_params, clean_request_payload

logger = logging.getLogger(__name__)


class Client(Session):
    """Welkin Health Client.

    Constructs a :obj:`requests.Session` for Welkin Health API requests with
    authorization, base URL, request timeouts, and request retries.

    Args:
        tenant (str): Name of the organization.
        instance (str): Name of the database inside a customer space.
        api_client (str): API client name.
        secret_key (str): API client secret key.
        timeout (int, optional): :obj:`TimeoutHTTPAdapter` timeout value. Defaults to 5.
        total (int, optional): :obj:`Retry` total value. Defaults to 5.
        backoff_factor (int, optional): :obj:`Retry` backoff_factor value.
            Defaults to 30.

    Usage::

        from welkin import Client

        welkin = Client(
            tenant="gh",
            instance="sb-demo",
            api_client="VBOPNRYRWJIP",
            secret_key="+}B{KGTG6#zG%P;tQm0C",
        )


        ### Patient methods
        patient = welkin.Patient(firstName="Foo", lastName="Bar").create()  # Create

        patient = welkin.Patient(id="6801d498-26f4-4aee-961b-5daffcf193c8").get()  # Read
        patients = welkin.Patients().get()  # Read all/list

        patient.update(firstName="Baz")  # Update
        patient.delete()  # Delete

        ### User methods
        user = client.User(username="bar", email="bar@foo.com").create()  # Create

        user = welkin.User(id="301b2895-cbf0-4cac-b4cf-1d082faee95c").get()  # Read
        users = welkin.Users().get()  # Read all/list
        uasers = welkin.Users().get(
            search="lightmatter", region="east-coast", seat_assigned=True, user_state="ACTIVE"
        )  # Filtered read all/list

        user.update(firstName="Baz")  # Update
        user.delete()  # Delete
    """

    def __init__(
        self,
        tenant,
        instance,
        api_client,
        secret_key,
        timeout=5,
        total=5,
        backoff_factor=30,
    ):
        """Welkin Health client constructor.

        Constructs a :obj:`requests.Session` for Welkin Health API requests with
        authorization, base URL, request timeouts, and request retries.

        Args:
            tenant (str): Name of the customer space.
            instance (str): Name of the database inside a customer space.
            api_client (str): API client name.
            secret_key (str): API client secret key.
            timeout (int, optional): :obj:`TimeoutHTTPAdapter` timeout value. Defaults to 5.
            total (int, optional): :obj:`Retry` total value. Defaults to 5.
            backoff_factor (int, optional): :obj:`Retry` backoff_factor value.
                Defaults to 30.
        """
        super().__init__()

        self.host = f"https://api.live.welkincloud.io/{tenant}/"
        self.headers.update({"User-Agent": f"python-welkin/{__version__}"})

        adapter = TimeoutHTTPAdapter(
            timeout=timeout,
            max_retries=Retry(
                total=total,
                status_forcelist=[429, 500, 502, 503, 504],
                backoff_factor=backoff_factor,
            ),
        )
        self.mount("https://", adapter)
        self.mount("http://", adapter)

        self.auth = WelkinAuth(
            tenant=tenant,
            api_client=api_client,
            secret_key=secret_key,
            token_method=self.get_token,
        )

        self.instance = instance
        self.__build_resources()

    def __build_resources(self) -> None:
        """Add each resource with a reference to this instance."""
        for k, v in globals().items():
            try:
                for base in v.__bases__:
                    if base.__name__ not in ["Collection", "Resource"]:
                        continue

                    v._client = self
                    setattr(self, k, v)

            except AttributeError:
                continue

    def prepare_request(self, request):
        if request.json:
            request.json = clean_request_payload(request.json)
        if request.params:
            request.params = clean_request_params(request.params)

        return super().prepare_request(request)

    def request(
        self,
        method: str,
        path: str,
        meta_key: str = None,
        meta_dict: dict = {},
        *args,
        **kwargs,
    ):
        """Override :obj:`Session` request method to add retries and output JSON.

        Args:
            method (str): Method for the new Request object.
            path (str): Path from host for the new Request object.

        Returns:
            dict: Response JSON
        """
        if not isinstance(path, str):
            path = "/".join((str(s) for s in path if s))
        path = path.rstrip("/")

        for _ in range(2):
            response = super().request(
                method=method, url=urljoin(self.host, path), *args, **kwargs
            )

            try:
                response.raise_for_status()
                break
            except HTTPError as exc:
                code = exc.response.status_code

                if code in [401]:
                    msg = response.json()
                    codes = ["NOT_VALID_JSON_WEB_TOKEN", "TOKEN_EXPIRED"]
                    if any(i.get("errorCode") in codes for i in msg):
                        self.auth.refresh_token()
                        continue

                raise WelkinHTTPError(exc) from exc

        try:
            json = response.json()
        except JSONDecodeError:
            if not response.content:
                return {}

            raise

        if isinstance(json, list):
            json = {
                "content": json,
                meta_key: meta_dict,
            }
        elif "rows" in json:
            json = {
                "content": json.pop("rows"),
                meta_key: meta_dict,
            }

        # Pull out the resource
        if "content" in json:
            resource = json.pop("content", None)
        else:
            resource = json.pop("data", None)

        meta = None

        # specifically with cdts the resource and metadata are both in the data dict
        if isinstance(resource, dict) and "content" in resource:
            new_resource = resource.pop("content", None)
            meta = resource.pop(meta_key, {})
            meta.update(json)
            meta.update(resource)
            resource = new_resource

        # Response metadata for pagination
        if meta_key:
            if not meta:
                meta = json.pop(meta_key, {})
            meta.update(json)
            return resource, meta

        return resource or json

    def get_token(self) -> dict:
        data = {"secret": self.auth.secret_key}
        response = self.post(f"admin/api_clients/{self.auth.api_client}", json=data)

        return response


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, timeout, *args, **kwargs):
        """TimeoutHTTPAdapter constructor.

        Args:
            timeout (int): How many seconds to wait for the server to send data before
                giving up.
        """
        self.timeout = timeout
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        """Override :obj:`HTTPAdapter` send method to add a default timeout."""
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout

        return super().send(request, **kwargs)
