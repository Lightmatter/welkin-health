import json
import os

import pytest

from welkin import Client

HEADER_BLACKLIST = [("Authorization", "API_TOKEN")]
POST_DATA_BLACKLIST = [("secret", "API_TOKEN")]
# REQUEST_BLACKLIST = ["secret"]
RESPONSE_BLACKLIST = ["token"]


@pytest.fixture(scope="module")
def vcr(vcr):
    vcr.filter_headers = HEADER_BLACKLIST
    vcr.filter_post_data_parameters = POST_DATA_BLACKLIST
    # vcr.before_record_request = scrub_request(REQUEST_BLACKLIST)
    vcr.before_record_response = scrub_response(RESPONSE_BLACKLIST)
    return vcr


# def scrub_request(blacklist, replacement="REDACTED"):
#     def before_record_request(request):
#         request.body = filter_body(request.body, blacklist, replacement)

#         return request

#     return before_record_request


def scrub_response(blacklist, replacement="REDACTED"):
    def before_record_response(response):
        response["body"]["string"] = filter_body(
            response["body"]["string"], blacklist, replacement
        )

        return response

    return before_record_response


def filter_body(body, blacklist, replacement):
    body_json = json.loads(body.decode())

    for k in body_json:
        if k in blacklist:
            body_json[k] = replacement

    return json.dumps(body_json).encode()


@pytest.fixture(scope="module", params=[False])
def client():
    """Get an authenticated Welkin API client."""
    return Client(
        tenant=os.environ["WELKIN_TENANT"],
        instance=os.environ["WELKIN_INSTANCE"],
        api_client=os.environ["WELKIN_API_CLIENT"],
        secret_key=os.environ["WELKIN_SECRET"],
    )
