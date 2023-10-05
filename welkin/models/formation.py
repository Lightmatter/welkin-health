from typing import Union

from welkin.models.base import Collection, Resource
from welkin.pagination import FormationIterator
from welkin.util import Target, _build_resources


class FormationBase:
    endpoint: str = None

    def __new__(cls, *args, **kwargs):
        if not cls.endpoint:
            raise AttributeError(
                f"The `endpoint` attribute must be set on {cls.__name__}"
            )

        return super().__new__(cls)


class FormationResource(FormationBase, Resource):
    def get(self, *args, **kwargs):
        return super().get(
            f"{self._formation._base_path}/{self.endpoint}/{self.name}",
            *args,
            **kwargs,
        )


class FormationCollection(FormationBase, Collection):
    resource = FormationResource
    iterator = FormationIterator

    def get(self, *args, **kwargs):
        return super().get(
            f"{self._formation._base_path}/{self.endpoint}",
            *args,
            **kwargs,
        )


class Assessment(FormationResource):
    endpoint = "assessments"


class Assessments(FormationCollection):
    resource = Assessment
    endpoint = "assessments"


class CDT(FormationResource):
    endpoint = "cdts"


class CDTs(FormationCollection):
    resource = CDT
    endpoint = "cdts"


class DocumentType(FormationResource):
    endpoint = "document-types"


class DocumentTypes(FormationCollection):
    resource = DocumentType
    endpoint = "document-types"


class EncounterDisposition(FormationResource):
    endpoint = "encounter-disposition"

    def __init__(self):
        super().__init__()

        self.name = ""


class Encounter(FormationResource):
    endpoint = "encounters"


class Encounters(FormationCollection):
    resource = Encounter
    endpoint = "encounters"


class Goal(FormationResource):
    endpoint = "goal-templates"


class Goals(FormationCollection):
    resource = Goal
    endpoint = "goal-templates"


class Program(FormationResource):
    endpoint = "programs"


class Programs(FormationCollection):
    resource = Program
    endpoint = "programs"


class Formation(Target):
    Assessment = Assessment
    Assessments = Assessments
    CDT = CDT
    CDTs = CDTs
    DocumentType = DocumentType
    DocumentTypes = DocumentTypes
    Encounter = Encounter
    EncounterDisposition = EncounterDisposition
    Encounters = Encounters
    Goal = Goal
    Goals = Goals
    Program = Program
    Programs = Programs

    def __init__(self, version: Union[int, str] = "current"):
        super().__init__()

        self._base_path = f"{self._client.instance}/formations/{version}"

        _build_resources(self, "_formation")
