import copy
import sys

import pytest

from welkin.util import (
    clean_date,
    clean_datetime,
    clean_json_list,
    clean_request_params,
    clean_request_payload,
    find_model_id,
    to_camel_case,
    to_snake_case,
)


class TestCleanRequestPayload:
    @pytest.fixture
    def payload(self, _uuid, base_date, utc_datetime, pst_datetime):
        return {
            "datetime": pst_datetime,
            "date": base_date,
            "dict": {
                "foo": "bar",
                "nested": {"date": base_date},
            },
            "list": [utc_datetime],
            "str": "Don't clean me please.",
            "int": [-sys.maxsize, 0, sys.maxsize],
            "float": [sys.float_info.min, 1, sys.float_info.max],
            "bool": [True, False],
            "_uuid4": _uuid,
            "none": None,
        }

    def test_clean_request_payload(
        self, payload, _uuid, pst_datetime_str, base_date_str, utc_datetime_str
    ):
        payload_copy = copy.deepcopy(payload)
        cleaned = clean_request_payload(payload)
        assert payload == payload_copy, "Payload was modified"

        assert cleaned["datetime"] == pst_datetime_str
        assert cleaned["date"] == base_date_str
        assert cleaned["dict"]["nested"]["date"] == base_date_str
        assert cleaned["list"][0] == utc_datetime_str
        assert cleaned["_uuid4"] == str(_uuid)


class TestCleanJsonList:
    @pytest.fixture
    def json_list(self, utc_datetime, base_date, pst_datetime):
        return [
            utc_datetime,
            base_date,
            [
                {
                    "foo": [pst_datetime],
                },
            ],
            "Strings don't get cleaned",
        ]

    def test_clean_json_list(
        self, json_list, utc_datetime_str, base_date_str, pst_datetime_str
    ):
        json_list_copy = copy.deepcopy(json_list)
        cleaned = clean_json_list(json_list)
        assert json_list == json_list_copy, "JSON list was modified"

        assert cleaned[0] == utc_datetime_str
        assert cleaned[1] == base_date_str
        assert cleaned[2][0]["foo"][0] == pst_datetime_str


class TestCleanRequestParams:
    @pytest.fixture
    def params(self, pst_datetime, base_date):
        return {
            "datetime": pst_datetime,
            "date": base_date,
            "list": ["foo", "bar", "baz"],
        }

    def test_clean_request_params(self, params, pst_datetime_str, base_date_str):
        params_copy = copy.deepcopy(params)
        cleaned = clean_request_params(params)
        assert params == params_copy, "Parameter dict was modified"

        assert cleaned["datetime"] == pst_datetime_str
        assert cleaned["date"] == base_date_str
        assert cleaned["list"] == "foo,bar,baz"


def test_clean_date(base_date, base_date_str):
    assert clean_date(base_date) == base_date_str


@pytest.mark.parametrize(
    "dt,expected",
    [
        (
            "utc_datetime",
            "utc_datetime_str",
        ),
        (
            "pst_datetime",
            "pst_datetime_str",
        ),
        (
            "est_datetime",
            "est_datetime_str",
        ),
    ],
)
def test_clean_datetime(dt, expected, request):
    cleaned = clean_datetime(request.getfixturevalue(dt))
    assert cleaned == request.getfixturevalue(expected)


@pytest.mark.parametrize(
    "input",
    [
        "foo_bar",
        "fooBar",
        "FooBar",
        "FOO_BAR",
        "fooBAR",
        "FOOBar",
    ],
)
def test_case_converters(input):
    assert to_camel_case(input) == "fooBar"
    assert to_snake_case(input) == "foo_bar"


def test_find_model_id(client):
    patient = client.Patient()
    encounter = patient.Encounter()

    with pytest.raises(AttributeError):
        find_model_id(encounter, "Patient")

    patient.id = "123"
    assert find_model_id(patient, "Patient") == patient.id
    assert find_model_id(encounter, "Patient") == patient.id

    del patient.id
    encounter.patientId = "456"
    assert find_model_id(encounter, "Patient") == encounter.patientId


def test_model_id(client):
    encounter = client.Patient().Encounter()
    with pytest.raises(TypeError) as exc_info:
        encounter.get()

    assert "missing 1 required positional argument" in exc_info.value.args[0]

    disposition = encounter.EncounterDisposition()
    with pytest.raises(TypeError) as exc_info:
        disposition.get()

    assert "missing 2 required positional arguments" in exc_info.value.args[0]
