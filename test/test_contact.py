from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from welkin.models import Contact

if TYPE_CHECKING:
    from welkin.models import PDT, Patient

RELATION = "Parent"


@pytest.fixture
def custodian(request, client, fixture_cassette) -> PDT:
    """A record of the contactable `pdt-custodian` PDT.

    Parametrized because Welkin allows only one contact per patient and PDT record pair.
    """
    with fixture_cassette():
        return client.PDT(id=request.param, pdtName="pdt-custodian").get()


@pytest.fixture
def contact_data(custodian: PDT) -> dict:
    """A contact's email and phone must match the fields of its PDT record."""
    return {
        "name": "Test Contact",
        "relation": RELATION,
        "pdtRecordId": custodian.id,
        "email": custodian.jsonBody["pdtf-email"],
        "emailPdtFieldName": "pdtf-email",
        "phone": custodian.jsonBody["pdtf-phone-number"],
        "phonePdtFieldName": "pdtf-phone-number",
    }


@pytest.mark.vcr
@pytest.mark.parametrize(
    "custodian",
    [pytest.param("dd5403c8-3fec-4335-8f5c-66cc6f91e1a1", id="custodian")],
    indirect=True,
)
def test_contact_create(patient: Patient, custodian: PDT, contact_data: dict, vcr_cassette):
    contact = patient.Contact(**contact_data).create()

    assert isinstance(contact, Contact)
    assert contact.id
    assert contact.patientId == patient.id
    assert contact.pdtRecordId == custodian.id
    assert contact.name == contact_data["name"]
    assert contact.relation == RELATION
    assert contact.email == custodian.jsonBody["pdtf-email"]
    assert contact.phone == custodian.jsonBody["pdtf-phone-number"]
    assert contact.active
    assert len(vcr_cassette) == 1


@pytest.mark.vcr
@pytest.mark.parametrize(
    "custodian",
    [pytest.param("fefa6f5f-176a-46be-b1ce-3184dab3233f", id="custodian")],
    indirect=True,
)
def test_contact_create_passing_patient_id(
    client, patient: Patient, custodian: PDT, contact_data: dict, vcr_cassette
):
    contact = client.Contact(**contact_data).create(patient_id=patient.id)

    assert isinstance(contact, Contact)
    assert contact.id
    assert contact.patientId == patient.id
    assert contact.pdtRecordId == custodian.id
    assert len(vcr_cassette) == 1
