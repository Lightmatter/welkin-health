from __future__ import annotations

import pytest

from welkin.exceptions import WelkinHTTPError
from welkin.models.email import Email, Emails

# The test environment recorded here has no Emails, but the tests do test for a specific
# response code from welkin and test whether the API calls complete without (expected)
# exceptions.


@pytest.mark.vcr
def test_email_patient_read(client, vcr_cassette):
    patient = client.Patient(id="371dd15c-cedc-4425-a394-d666c8d3fc01")

    email = patient.Email(id="2a8ac491-19bf-4812-9197-dffc2d42cfcf")
    assert isinstance(email, Email)
    assert email.id == "2a8ac491-19bf-4812-9197-dffc2d42cfcf"

    with pytest.raises(WelkinHTTPError) as excinfo:
        email.get()
    assert excinfo.value.response.status_code == 404
    assert len(vcr_cassette) == 1


@pytest.mark.vcr
def test_emails_patient_list(client, vcr_cassette):
    patient = client.Patient(id="371dd15c-cedc-4425-a394-d666c8d3fc01")

    emails = patient.Emails().get()

    assert isinstance(emails, Emails)
    assert len(emails) == 0
