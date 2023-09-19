import sys
import uuid
from datetime import date, datetime, timedelta, timezone

from welkin.util import (
    clean_date,
    clean_datetime,
    clean_json_list,
    clean_request_params,
    clean_request_payload,
)

UTC = timezone.utc
PST = timezone(timedelta(hours=-8))
EST = timezone(timedelta(hours=-5))


def test_clean_request_payload():
    payload = {
        "datetime": datetime(2022, 9, 15, 23, 0, 0, 0, PST),
        "date": date(2022, 9, 15),
        "dict": {"foo": "bar", "nested": {"date": date(2022, 9, 15)}},
        "list": [datetime(2022, 9, 15, 23, 0, 0, 0, UTC)],
        "str": "Don't clean me please.",
        "int": [-sys.maxsize, 0, sys.maxsize],
        "float": [sys.float_info.min, 1, sys.float_info.max],
        "bool": [True, False],
        "uuid4": uuid.uuid4(),
        "none": None,
    }
    payload_copy = dict(payload)

    cleaned = clean_request_payload(payload)
    assert payload == payload_copy, "Payload was modified"

    assert cleaned["datetime"] == "2022-09-16T07:00:00.000Z"
    assert cleaned["date"] == "2022-09-15T00:00:00.000Z"
    assert cleaned["dict"]["nested"]["date"] == "2022-09-15T00:00:00.000Z"
    assert cleaned["list"][0] == "2022-09-15T23:00:00.000Z"
    assert isinstance(cleaned["uuid4"], str)


def test_clean_json_list():
    json_list = [
        datetime(2022, 9, 15, 23, 0, 0, 0, UTC),
        date(2022, 9, 15),
        [
            {
                "foo": [datetime(2022, 9, 15, 23, 0, 0, 0, PST)],
            },
        ],
        "Strings don't get cleaned",
    ]
    json_list_copy = list(json_list)

    cleaned = clean_json_list(json_list)
    assert json_list == json_list_copy, "JSON list was modified"

    assert cleaned[0] == "2022-09-15T23:00:00.000Z"
    assert cleaned[1] == "2022-09-15T00:00:00.000Z"
    assert cleaned[2][0]["foo"][0] == "2022-09-16T07:00:00.000Z"


def test_clean_request_params():
    params = {
        "datetime": datetime(2022, 9, 15, 23, 0, 0, 0, PST),
        "date": date(2022, 9, 15),
        "list": ["foo", "bar", "baz"],
    }
    params_copy = dict(params)
    cleaned = clean_request_params(params)

    assert params == params_copy, "Parameter dict was modified"

    assert cleaned["datetime"] == "2022-09-16T07:00:00.000Z"
    assert cleaned["date"] == "2022-09-15T00:00:00.000Z"
    assert cleaned["list"] == "foo,bar,baz"


def test_clean_date():
    cleaned = clean_date(date(2022, 9, 15))

    assert cleaned == "2022-09-15T00:00:00.000Z"


def test_clean_datetime():
    datetime_tests = {
        "utc": {
            "dt": datetime(2022, 9, 15, 23, 0, 0, 0, UTC),
            "expected": "2022-09-15T23:00:00.000Z",
        },
        "pst": {
            "dt": datetime(2022, 9, 15, 23, 0, 0, 0, PST),
            "expected": "2022-09-16T07:00:00.000Z",
        },
        "est": {
            "dt": datetime(2022, 9, 15, 23, 0, 0, 0, EST),
            "expected": "2022-09-16T04:00:00.000Z",
        },
    }
    timedelta()
    for name, data in datetime_tests.items():
        cleaned = clean_datetime(data["dt"])
        assert cleaned == data["expected"], f"Unexpected result for '{name}'"
