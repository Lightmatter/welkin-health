from enum import Enum

from welkin.models.base import Collection, Resource
from welkin.pagination import FormationIterator


class AssessmentFormation(Resource):
    def get(self, *args, **kwargs):
        return super().get(
            f"{self._client.instance}/formations/current/assessments/{self.name}",
            *args,
            **kwargs,
        )


class AssessmentFormations(Collection):
    resource = AssessmentFormation
    iterator = FormationIterator

    def get(self, *args, **kwargs):
        return super().get(
            f"{self._client.instance}/formations/current/assessments",
            *args,
            **kwargs,
        )


class CDTFormation(Resource):
    def get(self, *args, **kwargs):
        return super().get(
            f"{self._client.instance}/formations/current/cdts/{self.name}",
            *args,
            **kwargs,
        )


class CDTFormations(Collection):
    resource = CDTFormation
    iterator = FormationIterator

    def get(self, *args, **kwargs):
        return super().get(
            f"{self._client.instance}/formations/current/cdts",
            *args,
            **kwargs,
        )


class DocumentTypeFormation(Resource):
    def get(self, *args, **kwargs):
        return super().get(
            f"{self._client.instance}/formations/current/document-types/{self.name}",
            *args,
            **kwargs,
        )


class DocumentTypeFormations(Collection):
    resource = DocumentTypeFormation
    iterator = FormationIterator

    def get(self, *args, **kwargs):
        return super().get(
            f"{self._client.instance}/formations/current/document-types",
            *args,
            **kwargs,
        )


class EncounterDispositionFormation(Resource):
    def get(self, version: int | str = "current", *args, **kwargs):
        return super().get(
            f"{self._client.instance}/formations/{version}/encounter-disposition/",
            *args,
            **kwargs,
        )


class EncounterFormation(Resource):
    def get(self, version: int | str = "current", *args, **kwargs):
        return super().get(
            f"{self._client.instance}/formations/{version}/encounters/{self.name}",
            *args,
            **kwargs,
        )


class EncounterFormations(Collection):
    iterator = FormationIterator
    resource = EncounterFormation

    def get(self, version: int | str = "current", *args, **kwargs):
        return super().get(
            f"{self._client.instance}/formations/{version}/encounters",
            *args,
            **kwargs,
        )


class GoalFormation(Resource):
    def get(self, *args, **kwargs):
        return super().get(
            f"{self._client.instance}/formations/current/goal-templates/{self.name}",
            *args,
            **kwargs,
        )


class GoalFormations(Collection):
    resource = GoalFormation
    iterator = FormationIterator

    def get(self, *args, **kwargs):
        return super().get(
            f"{self._client.instance}/formations/current/goal-templates",
            *args,
            **kwargs,
        )
