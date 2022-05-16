import pytest
from requests import Request


def auth_class(client):
    auth = client.auth
    auth.token_method = lambda: {"token": "API_TOKEN"}

    return auth


def test_token_get(client):
    auth = auth_class(client)
    token = auth.token

    assert token is not None


def test_token_refresh(client):
    auth = auth_class(client)

    token = f"{auth.token}_1"
    auth.refresh_token()

    assert token != auth.token


def test_auth_call(client):
    req = Request("GET", "https://foo.com/bar")
    prepped = req.prepare()

    auth = auth_class(client)
    auth(prepped)

    assert "Authorization" in prepped.headers


def test_auth_token_call(client):
    req = Request("GET", "https://foo.com/bar/api_clients")
    prepped = req.prepare()

    auth = auth_class(client)
    auth(prepped)

    assert "Authorization" not in prepped.headers
