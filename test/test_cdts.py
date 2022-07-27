import pytest

from welkin.exceptions import WelkinHTTPError
from welkin.models.cdt import CDT, CDTs


@pytest.mark.vcr()
def test_cdt_create(client, vcr_cassette):
    patient = client.Patient(id="3ff322fd-b504-4784-9798-0c7c8a4fdfb8")

    cdt = patient.CDT(cdtName="cdt-self-care", **{"cdtf-alone-time": "Yes"}).create()

    assert isinstance(cdt, CDT)
    assert hasattr(cdt, "id")
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_all_cdts_patient_read(client, vcr_cassette):
    patient = client.Patient(id="3ff322fd-b504-4784-9798-0c7c8a4fdfb8")
    cdts = patient.CDTs().get(cdt_name="cdt-self-care")

    assert isinstance(cdts, CDTs)
    assert isinstance(cdts[0], CDT)

    if len(cdts) > 20:
        assert len(vcr_cassette) > 1, "Pagination was expected"
    else:
        assert len(vcr_cassette) == 1, "Unexpected pagination"


@pytest.mark.vcr()
def test_cdt_patient_read(client, vcr_cassette):
    patient = client.Patient(id="3ff322fd-b504-4784-9798-0c7c8a4fdfb8")

    cdt = patient.CDT(
        cdtName="cdt-self-care", id="20a1cd2c-dd70-4589-afc4-fb99adaa25ad"
    ).get()

    assert isinstance(cdt, CDT)
    assert cdt.id == "20a1cd2c-dd70-4589-afc4-fb99adaa25ad"
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_cdt_update(client, vcr_cassette):
    patient = client.Patient(id="3ff322fd-b504-4784-9798-0c7c8a4fdfb8")
    cdt = patient.CDT(
        cdtName="cdt-self-care", id="20a1cd2c-dd70-4589-afc4-fb99adaa25ad"
    ).get()
    alone_time_response = cdt.jsonBody["cdtf-alone-time"]
    cdt.update(**{"cdtf-alone-time": "No"})
    assert cdt.jsonBody["cdtf-alone-time"] != alone_time_response
    assert len(vcr_cassette) == 2


@pytest.mark.vcr()
def test_cdt_bulk_update(client, vcr_cassette):
    patient = client.Patient(id="3ff322fd-b504-4784-9798-0c7c8a4fdfb8")
    cdt_1 = patient.CDT(
        cdtName="cdt-self-care", id="20a1cd2c-dd70-4589-afc4-fb99adaa25ad"
    ).get()
    cdt_2 = patient.CDT(
        cdtName="cdt-self-care", id="28f59572-efec-4ac1-bbfe-660b1abbd9e5"
    ).get()

    resp_1 = "Yes" if cdt_1.jsonBody["cdtf-alone-time"] == "No" else "Yes"
    resp_2 = "Yes" if cdt_2.jsonBody["cdtf-alone-time"] == "No" else "Yes"

    data = {
        "rows": [
            {
                "id": "20a1cd2c-dd70-4589-afc4-fb99adaa25ad",
                "jsonBody": {
                    "cdtf-alone-time": resp_1,
                },
            },
            {
                "id": "28f59572-efec-4ac1-bbfe-660b1abbd9e5",
                "jsonBody": {"cdtf-alone-time": resp_2},
            },
        ]
    }

    updated = patient.CDTs().update(cdt_name="cdt-self-care", body=data)
    assert updated[0].jsonBody["cdtf-alone-time"] == resp_1
    assert updated[1].jsonBody["cdtf-alone-time"] == resp_2
    assert len(vcr_cassette) == 3


@pytest.mark.vcr()
def test_cdt_delete(client, vcr_cassette):
    patient = client.Patient(id="3ff322fd-b504-4784-9798-0c7c8a4fdfb8")
    cdt = patient.CDT(
        cdtName="cdt-self-care", id="20a1cd2c-dd70-4589-afc4-fb99adaa25ad"
    ).get()

    cdt.delete()

    with pytest.raises(WelkinHTTPError) as excinfo:
        cdt.get()

        assert excinfo.value.response.status_code == 404

    assert len(vcr_cassette) == 3
