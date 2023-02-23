from enum import Enum

from welkin.models.base import Collection
from welkin.pagination import FormationIterator


class FormationDataType(Enum):
    cdts = "cdts"
    assessments = "assessments"
    encounters = "encounters"
    encounter_disposition = "encounter-disposition"
    care_plan = "goal-templates"
    document_types = "document-types"


class Formations(Collection):
    iterator = FormationIterator

    def get(self, data_type: str, *args, **kwargs):
        return super().get(
            f"{self._client.instance}/formations/current/{FormationDataType[data_type].value}",
            *args,
            **kwargs,
        )
