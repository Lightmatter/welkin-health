from __future__ import annotations

import pytest

from welkin.exceptions import WelkinHTTPError
from welkin.models import PDT, PDTs


@pytest.mark.vcr
def test_pdt_create(client, vcr_cassette):
    pdt = client.PDT(**{"pdtf-name": "Test Name"}).create(pdt_name="pdt-hospitals")

    assert isinstance(pdt, PDT)
    assert hasattr(pdt, "id")
    assert len(vcr_cassette) == 1


@pytest.mark.vcr
def test_pdt_read(client, vcr_cassette):
    pdt_id = "5af5cd13-9afe-49da-8e8c-a76f3637e83a"
    pdt = client.PDT(id=pdt_id, pdtName="pdt-hospitals").get()

    assert isinstance(pdt, PDT)
    assert pdt.id == pdt_id
    assert len(vcr_cassette) == 1


@pytest.mark.vcr
def test_pdt_read_all(client, vcr_cassette):
    pdts = client.PDTs().get(pdt_name="pdt-hospitals", size=1)

    assert isinstance(pdts, PDTs)
    assert isinstance(pdts[0], PDT)

    if len(pdts) > 20:
        assert len(vcr_cassette) > 1, "Pagination was expected"
    else:
        assert len(vcr_cassette) == 1, "Unexpected pagination"


@pytest.mark.vcr
def test_pdt_update(client, vcr_cassette):
    pdt = client.PDT(id="092ae416-1c0d-4e14-be22-9cc8dafacdbd").get()
    name = pdt.firstName

    pdt.update(firstName="Baz")

    assert pdt.firstName != name
    assert len(vcr_cassette) == 2


@pytest.mark.vcr
def test_pdt_delete(client, vcr_cassette):
    pdt = client.PDT(id="092ae416-1c0d-4e14-be22-9cc8dafacdbd")

    with pytest.raises(WelkinHTTPError) as excinfo:
        pdt.delete()

    assert excinfo.value.response.status_code == 403

    assert len(vcr_cassette) == 1
