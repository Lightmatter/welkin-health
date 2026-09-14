from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from welkin.models.audit import DataAudit, DataAudits, WebhookAudit, WebhookAudits

if TYPE_CHECKING:
    from welkin import Client


@pytest.mark.vcr
def test_webhook_audit_read_all(client: Client, vcr_cassette):
    events = client.WebhookAudits().get()

    assert isinstance(events, WebhookAudits)
    assert isinstance(events[0], WebhookAudit)

    if len(events) > 20:
        assert len(vcr_cassette) > 1, "Pagination was expected"
    else:
        assert len(vcr_cassette) == 1, "Unexpected pagination"


@pytest.mark.vcr
def test_data_audit_read_all(client: Client, vcr_cassette):
    events = client.DataAudits().get()

    assert isinstance(events, DataAudits)
    assert isinstance(events[0], DataAudit)

    if len(events) > 20:
        assert len(vcr_cassette) > 1, "Pagination was expected"
    else:
        assert len(vcr_cassette) == 1, "Unexpected pagination"
