import json
import os
import uuid

import pytest

from welkin import Client


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

    return vcr


def scrub_request(blacklist, replacement="REDACTED"):
    def before_record_request(request):
        # request.body = filter_body(request.body, blacklist, replacement)
        if "api_clients" in request.path:
            return None

        for k, v in blacklist.items():
            request.uri = request.uri.replace(v, f"{k}_{replacement}")

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
    body_json = json.loads(body.decode(), object_hook=object_hook)

    return json.dumps(body_json).encode()


def body_hook(blacklist, replacement):
    def hook(dct):
        for k in dct:
            if k in blacklist:
                dct[k] = redact(k, replacement)

        return dct

    return hook
