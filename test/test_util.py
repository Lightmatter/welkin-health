from datetime import date, datetime

import pytest

from welkin.util import (
    clean_date,
    clean_datetime,
    clean_json_list,
    clean_request_params,
    clean_request_payload,
)


def test_clean_request_payload():
    payload = {
        "datetime": datetime.fromisoformat("2022-09-15T23:00:00.000-08:00"),
        "date": date(2022, 9, 15),
        "dict": {"foo": "bar", "nested": {"date": date(2022, 9, 15)}},
        "list": [datetime.fromisoformat("2022-09-15T23:00:00.000+00:00")],
    }
    payload_copy = dict(payload)

    cleaned = clean_request_payload(payload)
    assert payload == payload_copy, "Payload was modified"

    assert cleaned["datetime"] == "2022-09-16T07:00:00.000Z"
    assert cleaned["date"] == "2022-09-15T07:00:00.000Z"
    assert cleaned["dict"]["nested"]["date"] == "2022-09-15T07:00:00.000Z"
    assert cleaned["list"][0] == "2022-09-15T23:00:00.000Z"


def test_clean_request_payload_invalid_type():
    with pytest.raises(TypeError):
        clean_request


def test_clean_json_list():
    json_list = [
        datetime.fromisoformat("2022-09-15T23:00:00.000+00:00"),
        date(2022, 9, 15),
        [
            {
                "foo": [datetime.fromisoformat("2022-09-15T23:00:00.000-08:00")],
            },
        ],
    ]
    json_list_copy = list(json_list)

    cleaned = clean_json_list(json_list)
    assert json_list == json_list_copy, "JSON list was modified"

    assert cleaned[0] == "2022-09-15T23:00:00.000Z"
    assert cleaned[1] == "2022-09-15T07:00:00.000Z"
    assert cleaned[2][0]["foo"][0] == "2022-09-16T07:00:00.000Z"


def test_clean_request_params():
    params = {
        "datetime": datetime.fromisoformat("2022-09-15T23:00:00.000-08:00"),
        "date": date(2022, 9, 15),
        "list": ["foo", "bar", "baz"],
    }
    params_copy = dict(params)
    cleaned = clean_request_params(params)

    assert params == params_copy, "Parameter dict was modified"

    assert cleaned["datetime"] == "2022-09-16T07:00:00.000Z"
    assert cleaned["date"] == "2022-09-15T07:00:00.000Z"
    assert cleaned["list"] == "foo,bar,baz"


def test_clean_date():
    cleaned = clean_date(date(2022, 9, 15))

    assert cleaned == "2022-09-15T07:00:00.000Z"


def test_clean_datetime():
    datetime_tests = {
        "utc": {
            "dt": datetime.fromisoformat("2022-09-15T23:00:00.000+00:00"),
            "expected": "2022-09-15T23:00:00.000Z",
        },
        "pst": {
            "dt": datetime.fromisoformat("2022-09-15T23:00:00.000-08:00"),
            "expected": "2022-09-16T07:00:00.000Z",
        },
        "est": {
            "dt": datetime.fromisoformat("2022-09-15T23:00:00.000-05:00"),
            "expected": "2022-09-16T04:00:00.000Z",
        },
    }

    for name, data in datetime_tests.items():
        cleaned = clean_datetime(data["dt"])
        assert cleaned == data["expected"], f"Unexpected result for '{name}'"
