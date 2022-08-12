import pytest

from welkin.models import CarePlan


@pytest.mark.vcr()
def test_care_plan_create(client, vcr_cassette):
    patient = client.Patient(id="173a8adf-92e8-4832-8900-027c71b0d768")

    overview_message = "This is a message for the overview."

    care_plan = patient.CarePlan(overview=overview_message)

    created_cp = care_plan.create()

    assert isinstance(created_cp, CarePlan)
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_care_plan_create_passing_patient_id(client, vcr_cassette):
    patient_id = "331678c1-0ec9-4e4a-a947-8147a1d067a5"
    overview_message = "This is a message for the overview."

    care_plan = client.CarePlan(overview=overview_message).create(patient_id=patient_id)

    assert isinstance(care_plan, CarePlan)
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_care_plan_read(client, vcr_cassette):
    patient = client.Patient(id="173a8adf-92e8-4832-8900-027c71b0d768")
    care_plan = patient.CarePlan().get()

    assert isinstance(care_plan, CarePlan)
    assert care_plan.id
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_care_plan_read_passing_patient_id(client, vcr_cassette):
    patient_id = "331678c1-0ec9-4e4a-a947-8147a1d067a5"
    care_plan = client.CarePlan().get(patient_id=patient_id)

    assert isinstance(care_plan, CarePlan)
    assert care_plan.id
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_care_plan_update(client, vcr_cassette):
    patient = client.Patient(id="173a8adf-92e8-4832-8900-027c71b0d768")
    care_plan = patient.CarePlan().get()
    overview = care_plan.patientOverview["overview"]
    new_overview = "A new overview message 123"
    care_plan.CarePlanOverview(**{"overview": new_overview}).update()
    care_plan = patient.CarePlan().get()

    assert care_plan.patientOverview["overview"] != overview
    assert care_plan.patientOverview["overview"] == new_overview
    assert len(vcr_cassette) == 3


@pytest.mark.vcr()
def test_care_plan_update_passing_patient_id(client, vcr_cassette):
    patient_id = "173a8adf-92e8-4832-8900-027c71b0d768"
    care_plan = client.CarePlan().get(patient_id=patient_id)
    overview = care_plan.patientOverview["overview"]
    new_overview = "Why not have a new overview message?"
    care_plan = client.CarePlanOverview(**{"overview": new_overview}).update(
        patient_id=patient_id
    )
    care_plan = client.CarePlan().get(patient_id=patient_id)

    assert care_plan.patientOverview["overview"] != overview
    assert care_plan.patientOverview["overview"] == new_overview
    assert len(vcr_cassette) == 3
