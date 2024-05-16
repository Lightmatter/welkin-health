from __future__ import annotations

import pytest


@pytest.mark.vcr
def test_cdt_records_export_read(client, vcr_cassette):
    export = client.CDTRecordsExport()

    exports = list(export.get(paginate=True, size=1000))

    assert len(exports) > 1
    assert len(vcr_cassette) == 6
