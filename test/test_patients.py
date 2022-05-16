import pytest

from welkin.exceptions import WelkinHTTPError
from welkin.models.patient import Patient, Patients


@pytest.mark.vcr()
def test_patient_create(client, vcr_cassette):
    patient = client.Patient(firstName="Foo", lastName="Bar").create()

    assert isinstance(patient, Patient)
    assert hasattr(patient, "id")
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_patient_read(client, vcr_cassette):
    patient_id = "092ae416-1c0d-4e14-be22-9cc8dafacdbd"
    patient = client.Patient(id=patient_id).get()

    assert isinstance(patient, Patient)
    assert patient.id == patient_id
    assert len(vcr_cassette) == 1


@pytest.mark.vcr()
def test_patient_read_all(client, vcr_cassette):
    patients = client.Patients().get()

    assert isinstance(patients, Patients)
    assert isinstance(patients[0], Patient)

    if len(patients) > 20:
        assert len(vcr_cassette) > 1, "Pagination was expected"
    else:
        assert len(vcr_cassette) == 1, "Unexpected pagination"


@pytest.mark.vcr()
def test_patient_update(client, vcr_cassette):
    patient = client.Patient(id="092ae416-1c0d-4e14-be22-9cc8dafacdbd").get()
    name = patient.firstName

    patient.update(firstName="Baz")

    assert patient.firstName != name
    assert len(vcr_cassette) == 2


@pytest.mark.vcr()
def test_patient_delete(client, vcr_cassette):
    patient = client.Patient(id="092ae416-1c0d-4e14-be22-9cc8dafacdbd")

    with pytest.raises(WelkinHTTPError) as excinfo:
        patient.delete()

    assert excinfo.value.response.status_code == 403

    assert len(vcr_cassette) == 1
