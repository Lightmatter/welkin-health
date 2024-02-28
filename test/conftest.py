import inspect
import json
import os
import uuid
from datetime import date, datetime, time, timedelta, timezone
from http import HTTPStatus
from pathlib import Path
from uuid import uuid4

import pytest

from welkin import Client
from welkin.exceptions import WelkinHTTPError


def pytest_collection_modifyitems(items):
    # Ensure auth tests execute first, otherwise all other tests will fail.
    items.sort(key=lambda x: True if "authentication" not in x.nodeid else False)


def redact(field_name, extra=""):
    parts = [field_name, extra, str(uuid.uuid4())]

    return "_".join(i for i in parts if i)


HEADER_BLACKLIST = [("Authorization", redact("API_TOKEN"))]
POST_DATA_BLACKLIST = [("secret", redact("API_TOKEN"))]
REQUEST_BLACKLIST = ["secret"]
RESPONSE_BLACKLIST = [
    "token",
    "createdBy",
    "createdByName",
    "updatedBy",
    "updatedByName",
]
CLIENT_INIT = dict(
    tenant=os.environ["WELKIN_TENANT"],
    instance=os.environ["WELKIN_INSTANCE"],
    api_client=os.environ["WELKIN_API_CLIENT"],
    secret_key=os.environ["WELKIN_SECRET"],
)


@pytest.fixture(scope="module")
def client():
    """Get an authenticated Welkin API client."""
    return Client(**CLIENT_INIT)


@pytest.fixture(scope="module")
def vcr(vcr):
    vcr.filter_headers = HEADER_BLACKLIST
    vcr.filter_post_data_parameters = POST_DATA_BLACKLIST
    vcr.before_record_request = scrub_request(CLIENT_INIT)
    vcr.before_record_response = scrub_response(RESPONSE_BLACKLIST)
    vcr.decode_compressed_response = True

    return vcr


def scrub_request(blacklist, replacement="REDACTED"):
    def before_record_request(request):
        # request.body = filter_body(request.body, blacklist, replacement)
        if "api_clients" in request.path:
            return None
        uri_comps = request.uri.split("/")
        for k, v in blacklist.items():
            try:
                ind = uri_comps.index(v)
                uri_comps[ind] = f"{k}_{replacement}"
            except ValueError:
                continue

        request.uri = "/".join(uri_comps)
        return request

    return before_record_request


def scrub_response(blacklist, replacement="REDACTED"):
    def before_record_response(response):
        response["body"]["string"] = filter_body(
            response["body"]["string"], blacklist, replacement
        )

        return response

    return before_record_response


def filter_body(body, blacklist, replacement):
    if not body:
        return body
    object_hook = body_hook(blacklist, replacement)
    try:
        body_json = json.loads(body.decode(), object_hook=object_hook)
        return json.dumps(body_json).encode()
    except UnicodeDecodeError:
        return body


def body_hook(blacklist, replacement):
    def hook(dct):
        for k in dct:
            if k in blacklist:
                dct[k] = redact(k, replacement)

        return dct

    return hook


@pytest.fixture
def fixture_cassette(vcr, vcr_cassette_dir, vcr_cassette_name):
    def _cassette():
        caller_function_name = inspect.stack()[1].function
        cassette_name = f"{caller_function_name}__{vcr_cassette_name}"
        fixture_path = str(Path(vcr_cassette_dir, "fixtures"))

        return vcr.use_cassette(cassette_name, cassette_library_dir=fixture_path)

    return _cassette


@pytest.fixture
def patient(client, fixture_cassette):
    patient = client.Patient(
        firstName="Test",
        lastName="Patient",
        email="test.patient@example.com",
        externalGuid=uuid.UUID("12345678-1234-1234-1234-1234567890ab"),
    )

    with fixture_cassette():
        try:
            return patient.get()
        except WelkinHTTPError as exc:
            if exc.response.status_code != HTTPStatus.NOT_FOUND:
                raise

            return patient.create()


@pytest.fixture
def base_date():
    return date(year=2022, month=9, day=15)


@pytest.fixture
def base_date_str():
    return "2022-09-15T00:00:00.000Z"


@pytest.fixture
def base_time():
    return time(hour=23, minute=0, second=0, microsecond=0)


@pytest.fixture
def utc_datetime(base_date, base_time):
    return datetime.combine(base_date, base_time, tzinfo=timezone.utc)


@pytest.fixture
def utc_datetime_str():
    return "2022-09-15T23:00:00.000Z"


@pytest.fixture
def pst_datetime(base_date, base_time):
    return datetime.combine(base_date, base_time, tzinfo=timezone(timedelta(hours=-8)))


@pytest.fixture
def pst_datetime_str():
    return "2022-09-16T07:00:00.000Z"


@pytest.fixture
def est_datetime(base_date, base_time):
    return datetime.combine(base_date, base_time, tzinfo=timezone(timedelta(hours=-5)))


@pytest.fixture
def est_datetime_str():
    return "2022-09-16T04:00:00.000Z"


@pytest.fixture
def _uuid():
    return uuid4()
