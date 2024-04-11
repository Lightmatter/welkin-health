from __future__ import annotations

import json

import pytest

from welkin.exceptions import WelkinHTTPError


@pytest.mark.vcr
def test_exception(client):
    url = "admin/users/me"
    with pytest.raises(WelkinHTTPError) as exc_info:
        client.get(url)

    exc = exc_info.value
    assert str(exc).endswith(json.dumps(exc.response.json(), indent=2))


@pytest.mark.vcr
def test_exception_no_json(client):
    url = "https://httpbin.org/status/400"
    with pytest.raises(WelkinHTTPError) as exc_info:
        client.get(url)

    exc = exc_info.value
    assert str(exc) == f"400 Client Error: BAD REQUEST for url: {url}"
