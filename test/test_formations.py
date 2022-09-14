import pytest

from welkin.models.base import Resource
from welkin.models.formation import FormationDataType, Formations


@pytest.mark.vcr()
def test_formation_get(client, vcr_cassette):
    for data_type in FormationDataType:
        formation_info = client.Formations().get(data_type)
        assert isinstance(formation_info, Formations)
        if len(formation_info) > 0:
            assert isinstance(formation_info[0], Resource)

    assert len(vcr_cassette) == len(FormationDataType)
