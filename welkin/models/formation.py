from enum import Enum

from welkin.models.base import Collection, Resource
from welkin.pagination import PageableIterator


class FormationDataType(Enum):
    CDTS = "cdts"
    ASSESSMENTS = "assessments"
    ENCOUNTERS = "encounters"
    CARE_PLAN = "goal-templates"


class Formations(Collection):
    iterator = PageableIterator

    def get(self, data_type: FormationDataType, version: str = "current", **kwargs):
        return super().get(
            f"{self._client.instance}/formations/{version}/{data_type.value}",
            params=kwargs,
        )
