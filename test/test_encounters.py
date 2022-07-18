from datetime import datetime, timedelta, timezone

import pytest

from welkin.exceptions import WelkinHTTPError
from welkin.models.encounter import Encounter, Encounters
from welkin.util import clean_datetime

UTC = timezone.utc


@pytest.mark.vcr()
def test_encounter_create(client, vcr_cassette):
    patient = client.Patient(id="0056c34b-9a83-41bd-bf4d-e4710d7a77f9")
    start = datetime.now(tz=UTC) + timedelta(hours=6)
    end = start + timedelta(hours=1)

    data = {
        "title": "new enc",
        "description": "new encounter",
        "templateName": "etmp-encounter1",
        "currentScheduledAppointment": {
            "eventType": "ENCOUNTER",
            "eventTitle": "NEW ENC",
            "startDateTime": clean_datetime(start),
            "endDateTime": clean_datetime(end),
            "hostId": "a9618392-799d-4664-a896-5f1756f8d336",
            "participants": [
                {
                    "participantId": "a9618392-799d-4664-a896-5f1756f8d336",
                    "participantRole": "psm",
                },
                {"participantId": patient.id, "participantRole": "patient"},
            ],
        },
    }

    encounter = patient.Encounter
    for k, v in data.items():
        encounter[k] = v

    created_enc = encounter.create()

    assert isinstance(created_enc, Encounter)
    assert hasattr(created_enc, "id")
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_all_encounters_patient_read(client, vcr_cassette):
    patient = client.Patient(id="0056c34b-9a83-41bd-bf4d-e4710d7a77f9")
    encounters = patient.Encounters.get()

    assert isinstance(encounters, Encounters)
    assert len(encounters) == 8
    assert isinstance(encounters[0], Encounter)
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_all_encounters_user_read(client, vcr_cassette):
    user = client.User(id="a9618392-799d-4664-a896-5f1756f8d336")
    encounters = user.Encounters.get(params={"withCareTeam": "false"})

    assert isinstance(encounters, Encounters)
    assert len(encounters) == 8
    assert isinstance(encounters[0], Encounter)
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_encounter_patient_read(client, vcr_cassette):
    patient = client.Patient(id="0056c34b-9a83-41bd-bf4d-e4710d7a77f9")

    encounter = patient.Encounter
    encounter["id"] = "72822eb2-8034-4822-bbc2-58caa0517eea"

    enc = encounter.get()

    assert isinstance(enc, Encounter)
    assert enc.id == "72822eb2-8034-4822-bbc2-58caa0517eea"
    assert len(vcr_cassette) == 1


@pytest.mark.skip(reason="getting an error about cdts")
@pytest.mark.vcr()
def test_encounter_update(client, vcr_cassette):
    patient = client.Patient(id="0056c34b-9a83-41bd-bf4d-e4710d7a77f9")

    encounter = patient.Encounter
    encounter["id"] = "72822eb2-8034-4822-bbc2-58caa0517eea"
    enc = encounter.get()
    notes = enc.notes

    enc.update(notes="a new note")

    assert enc.notes != notes
    assert len(vcr_cassette) == 2


@pytest.mark.vcr()
def test_encounter_delete(client, vcr_cassette):
    patient = client.Patient(id="0056c34b-9a83-41bd-bf4d-e4710d7a77f9")

    encounter = patient.Encounter
    encounter["id"] = "72822eb2-8034-4822-bbc2-58caa0517eea"

    enc = encounter.get()
    enc.delete()

    with pytest.raises(WelkinHTTPError) as excinfo:
        enc.get()

        assert excinfo.value.response.status_code == 404

    assert len(vcr_cassette) == 3
