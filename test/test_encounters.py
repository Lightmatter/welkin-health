from datetime import datetime, timedelta, timezone

import pytest

from welkin.exceptions import WelkinHTTPError
from welkin.models.encounter import Encounter, Encounters

UTC = timezone.utc


@pytest.mark.vcr()
def test_encounter_create(client, vcr_cassette):
    patient = client.Patient(id="371dd15c-cedc-4425-a394-d666c8d3fc01")
    start = datetime.now(tz=UTC) + timedelta(hours=6)
    end = start + timedelta(hours=1)

    data = {
        "title": "new enc",
        "description": "new encounter",
        "templateName": "etmp-initial-consultation",
        "currentScheduledAppointment": {
            "eventType": "ENCOUNTER",
            "eventTitle": "NEW ENC",
            "startDateTime": start,
            "endDateTime": end,
            "hostId": "c08af975-8afc-49cb-84ac-7189b727148c",
            "participants": [
                {
                    "participantId": "c08af975-8afc-49cb-84ac-7189b727148c",
                    "participantRole": "psm",
                },
                {"participantId": patient.id, "participantRole": "patient"},
            ],
        },
    }

    encounter = patient.Encounter(**data)

    created_enc = encounter.create()

    assert isinstance(created_enc, Encounter)
    assert hasattr(created_enc, "id")
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_all_encounters_patient_read(client, vcr_cassette):
    patient = client.Patient(id="371dd15c-cedc-4425-a394-d666c8d3fc01")
    encounters = patient.Encounters().get()

    assert isinstance(encounters, Encounters)
    assert isinstance(encounters[0], Encounter)

    if len(encounters) > 20:
        assert len(vcr_cassette) > 1, "Pagination was expected"
    else:
        assert len(vcr_cassette) == 1, "Unexpected pagination"


@pytest.mark.vcr()
def test_all_encounters_user_read(client, vcr_cassette):
    user = client.User(id="c08af975-8afc-49cb-84ac-7189b727148c")
    encounters = user.Encounters().get(with_care_team=False)

    assert isinstance(encounters, Encounters)
    assert isinstance(encounters[0], Encounter)

    if len(encounters) > 20:
        assert len(vcr_cassette) > 1, "Pagination was expected"
    else:
        assert len(vcr_cassette) == 1, "Unexpected pagination"


@pytest.mark.vcr()
def test_encounter_patient_read(client, vcr_cassette):
    patient = client.Patient(id="371dd15c-cedc-4425-a394-d666c8d3fc01")

    encounter = patient.Encounter(id="2a8ac491-19bf-4812-9197-dffc2d42cfcf").get()

    assert isinstance(encounter, Encounter)
    assert encounter.id == "2a8ac491-19bf-4812-9197-dffc2d42cfcf"
    assert len(vcr_cassette) == 1


# @pytest.mark.skip(reason="getting an error about cdts")
@pytest.mark.vcr()
def test_encounter_update(client, vcr_cassette):
    patient = client.Patient(id="371dd15c-cedc-4425-a394-d666c8d3fc01")

    encounter = patient.Encounter(id="22c26a65-161f-42c3-bb0f-a976dac8afe6").get()
    notes = encounter.jsonBody["notes"]

    encounter.update(notes="a newer note")

    assert encounter.jsonBody["notes"] != notes
    assert len(vcr_cassette) == 2


@pytest.mark.vcr()
def test_encounter_delete(client, vcr_cassette):
    patient = client.Patient(id="371dd15c-cedc-4425-a394-d666c8d3fc01")

    encounter = patient.Encounter(id="2a8ac491-19bf-4812-9197-dffc2d42cfcf").get()

    encounter.delete()

    with pytest.raises(WelkinHTTPError) as excinfo:
        encounter.get()

        assert excinfo.value.response.status_code == 404

    assert len(vcr_cassette) == 3
