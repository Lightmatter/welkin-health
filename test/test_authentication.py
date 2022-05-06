import pytest
from requests import Request


@pytest.mark.vcr()
def test_token_get(client, vcr_cassette):
    auth = client.auth
    token = auth.token

    assert token is not None
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_token_refresh(client, vcr_cassette):
    auth = client.auth

    token = f"{auth.token}_1"
    auth.refresh_token()

    assert token != auth.token
    assert len(vcr_cassette) == 2


def test_auth_call(client):
    req = Request("GET", "https://foo.com/bar")
    prepped = req.prepare()

    auth = client.auth
    auth(prepped)

    assert "Authorization" in prepped.headers


def test_auth_token_call(client):
    req = Request("GET", "https://foo.com/bar/api_clients")
    prepped = req.prepare()

    auth = client.auth
    auth(prepped)

    assert "Authorization" not in prepped.headers
