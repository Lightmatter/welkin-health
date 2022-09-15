from enum import Enum

from welkin.models.base import Collection
from welkin.pagination import FormationIterator


class FormationDataType(Enum):
    CDTS = "cdts"
    ASSESSMENTS = "assessments"
    ENCOUNTERS = "encounters"
    ENCOUNTER_DISPOSITION = "encounter-disposition"
    CARE_PLAN = "goal-templates"


class Formations(Collection):
    iterator = FormationIterator

    def get(self, data_type: FormationDataType, *args, **kwargs):
        return super().get(
            f"{self._client.instance}/formations/current/{data_type.value}",
            *args,
            **kwargs,
        )
