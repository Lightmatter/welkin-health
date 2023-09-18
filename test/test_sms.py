import pytest

from welkin.exceptions import WelkinHTTPError
from welkin.models.sms import SMS, SMSes

# The test environment recorded here has no SMSes, but the tests do test for a specific
# response code from welkin and test whether the API calls complete without (expected)
# exceptions.


@pytest.mark.vcr
def test_sms_patient_read(client, vcr_cassette):
    patient = client.Patient(id="371dd15c-cedc-4425-a394-d666c8d3fc01")

    sms = patient.SMS(id="2a8ac491-19bf-4812-9197-dffc2d42cfcf")
    assert isinstance(sms, SMS)
    assert sms.id == "2a8ac491-19bf-4812-9197-dffc2d42cfcf"

    with pytest.raises(WelkinHTTPError) as excinfo:
        sms.get()
    assert excinfo.value.response.status_code == 404
    assert len(vcr_cassette) == 1


@pytest.mark.vcr
def test_smses_patient_list(client, vcr_cassette):
    patient = client.Patient(id="371dd15c-cedc-4425-a394-d666c8d3fc01")

    smses = patient.SMSes().get()

    assert isinstance(smses, SMSes)
    assert len(smses) == 0
