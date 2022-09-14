from enum import Enum

from welkin.models.base import Collection
from welkin.pagination import PageableIterator


class FormationDataType(Enum):
    CDTS = "cdts"
    ASSESSMENTS = "assessments"
    ENCOUNTERS = "encounters"
    ENCOUNTER_DISPOSITION = "encounter-disposition"
    CARE_PLAN = "goal-templates"


class Formations(Collection):
    iterator = PageableIterator

    def get(self, data_type: FormationDataType, **kwargs):
        return super().get(
            f"{self._client.instance}/formations/current/{data_type.value}",
            params=kwargs,
        )
