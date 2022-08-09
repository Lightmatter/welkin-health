from datetime import datetime, timedelta, timezone

import pytest

from welkin.exceptions import WelkinHTTPError
from welkin.models.assessment import Assessment, Assessments
from welkin.models.encounter import Disposition, Encounter, Encounters
from welkin.models.user import User

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


@pytest.mark.vcr()
def test_encounter_patient_read_related_data(client, vcr_cassette):
    patient = client.Patient(id="371dd15c-cedc-4425-a394-d666c8d3fc01")

    encounter = patient.Encounter(id="22c26a65-161f-42c3-bb0f-a976dac8afe6").get(
        related_data=True
    )

    assert isinstance(encounter, Encounter)
    assert isinstance(encounter.userRelatedToCalendarEvent, User)
    assert len(vcr_cassette) == 1


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


@pytest.mark.vcr()
def test_encounter_assessments(client, vcr_cassette):
    patient = client.Patient(id="371dd15c-cedc-4425-a394-d666c8d3fc01")

    encounter = patient.Encounter(id="22c26a65-161f-42c3-bb0f-a976dac8afe6").get(
        related_data=True
    )

    assert isinstance(encounter, Encounter)
    assert isinstance(encounter.assessmentLinks, Assessments)
    assert isinstance(encounter.assessmentLinks[0], Assessment)
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_encounter_assessments_get(client, vcr_cassette):
    patient = client.Patient(id="371dd15c-cedc-4425-a394-d666c8d3fc01")

    encounter = patient.Encounter(id="22c26a65-161f-42c3-bb0f-a976dac8afe6").get()
    assessments = encounter.Assessments().get()

    assert isinstance(assessments, Assessments)
    assert isinstance(assessments[0], Assessment)
    assert len(vcr_cassette) == 2


# these tests show all of the ways one could get an Encounter Assessment
@pytest.mark.vcr()
def test_encounter_assessment_get(client, vcr_cassette):
    patient = client.Patient(id="371dd15c-cedc-4425-a394-d666c8d3fc01")

    encounter = patient.Encounter(id="22c26a65-161f-42c3-bb0f-a976dac8afe6")
    assessment = encounter.Assessment(id="7cf6baa2-14d5-4d3a-9416-0ddd729644b8").get()

    assert isinstance(assessment, Assessment)
    assert assessment.id == "7cf6baa2-14d5-4d3a-9416-0ddd729644b8"
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_encounter_get_assessment_get(client, vcr_cassette):
    patient = client.Patient(id="371dd15c-cedc-4425-a394-d666c8d3fc01")

    encounter = patient.Encounter(id="22c26a65-161f-42c3-bb0f-a976dac8afe6").get()
    assessment = encounter.Assessment(id="10c6481b-f25b-49cf-9761-33aeced25f46").get()

    assert isinstance(assessment, Assessment)
    assert assessment.id == "10c6481b-f25b-49cf-9761-33aeced25f46"
    assert len(vcr_cassette) == 2


@pytest.mark.vcr()
def test_assessment_get(client, vcr_cassette):
    assessment = client.Assessment(id="10c6481b-f25b-49cf-9761-33aeced25f46").get(
        patient_id="371dd15c-cedc-4425-a394-d666c8d3fc01",
        encounter_id="22c26a65-161f-42c3-bb0f-a976dac8afe6",
    )
    assert isinstance(assessment, Assessment)
    assert assessment.id == "10c6481b-f25b-49cf-9761-33aeced25f46"
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_encounter_related_data_assessment_get(client, vcr_cassette):
    patient = client.Patient(id="371dd15c-cedc-4425-a394-d666c8d3fc01")

    encounter = patient.Encounter(id="22c26a65-161f-42c3-bb0f-a976dac8afe6").get(
        related_data=True
    )
    assessment = encounter.assessmentLinks[-1].get()

    assert isinstance(assessment, Assessment)
    assert assessment.id == "10c6481b-f25b-49cf-9761-33aeced25f46"
    assert len(vcr_cassette) == 2


@pytest.mark.vcr()
def test_encounter_assessment_create(client, vcr_cassette):
    patient = client.Patient(id="371dd15c-cedc-4425-a394-d666c8d3fc01")

    encounter = patient.Encounter(id="22c26a65-161f-42c3-bb0f-a976dac8afe6")
    assessment = encounter.Assessment(assessmentName="asm-hello-form2").create()

    assert isinstance(assessment, Assessment)
    assert hasattr(assessment, "id")
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_encounter_assessment_update(client, vcr_cassette):
    patient = client.Patient(id="371dd15c-cedc-4425-a394-d666c8d3fc01")

    encounter = patient.Encounter(id="22c26a65-161f-42c3-bb0f-a976dac8afe6")

    assessment = encounter.Assessment(id="4d2be3ba-2be3-4171-a8bf-de68cd8e5a42").get()
    assessment_record_id = assessment.jsonBody["assessmentRecordId"]

    assessment.update(assessmentRecordId="e18a2759-5089-44e7-9d31-cf942476ffab")

    assert isinstance(assessment, Assessment)
    assert assessment.jsonBody["assessmentRecordId"] != assessment_record_id
    assert len(vcr_cassette) == 2


@pytest.mark.vcr()
def test_encounter_assessment_delete(client, vcr_cassette):
    patient = client.Patient(id="371dd15c-cedc-4425-a394-d666c8d3fc01")

    encounter = patient.Encounter(id="22c26a65-161f-42c3-bb0f-a976dac8afe6")
    assessment = encounter.Assessment(id="4d2be3ba-2be3-4171-a8bf-de68cd8e5a42")

    assessment.delete()
    with pytest.raises(WelkinHTTPError) as excinfo:
        assessment.get()

        assert excinfo.value.response.status_code == 404

    assert len(vcr_cassette) == 2


@pytest.mark.vcr()
def test_encounter_disposition_get_nested(client, vcr_cassette):
    patient = client.Patient(id="173a8adf-92e8-4832-8900-027c71b0d768")
    encounter = patient.Encounter(id="d6f4b66e-1be6-403a-ae47-1bbcee264c5e").get(
        related_data=True
    )
    disposition = encounter.disposition

    assert isinstance(disposition, Disposition)
    assert hasattr(disposition, "id")
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_encounter_disposition_get(client, vcr_cassette):
    patient = client.Patient(id="173a8adf-92e8-4832-8900-027c71b0d768")
    encounter = patient.Encounter(id="d6f4b66e-1be6-403a-ae47-1bbcee264c5e")
    disposition = encounter.Disposition().get()

    assert isinstance(disposition, Disposition)
    assert disposition.id == "8cd87974-b1cb-4a6f-8873-71d5d188c4aa"
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_encounter_disposition_get_patient_id_encounter_id(client, vcr_cassette):
    disposition = client.Disposition().get(
        patient_id="173a8adf-92e8-4832-8900-027c71b0d768",
        encounter_id="d6f4b66e-1be6-403a-ae47-1bbcee264c5e",
    )
    assert isinstance(disposition, Disposition)
    assert disposition.id == "8cd87974-b1cb-4a6f-8873-71d5d188c4aa"
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_encounter_disposition_update(client, vcr_cassette):
    patient = client.Patient(id="173a8adf-92e8-4832-8900-027c71b0d768")
    encounter = patient.Encounter(id="d6f4b66e-1be6-403a-ae47-1bbcee264c5e")
    disposition = encounter.Disposition(id="8cd87974-b1cb-4a6f-8873-71d5d188c4aa").get()

    review = disposition.jsonBody["uicedf-review"]

    disposition.update(**{"uicedf-review": "great health"})

    assert disposition.jsonBody["uicedf-review"] != review
    assert len(vcr_cassette) == 2
