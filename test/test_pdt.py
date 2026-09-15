from __future__ import annotations

import pytest

from welkin.models import PDT


@pytest.mark.vcr
def test_pdt_create(client, vcr_cassette):
    pdt = client.PDT(**{"pdtf-name": "Test Name"}).create(pdt_name="pdt-hospitals")

    assert isinstance(pdt, PDT)
    assert hasattr(pdt, "id")
    assert len(vcr_cassette) == 1


@pytest.mark.vcr
def test_pdt_read(client, vcr_cassette):
    pdt_id = "213ddaef-7914-4f46-8327-e2a343a4e7f6"
    pdt = client.PDT(id=pdt_id, pdtName="pdt-hospitals").get()

    assert isinstance(pdt, PDT)
    assert pdt.id == pdt_id
    assert len(vcr_cassette) == 1
