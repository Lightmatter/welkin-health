from enum import Enum

from welkin.models.assessment import Assessment, Assessments
from welkin.models.base import Collection, Resource
from welkin.pagination import MetaInfoIterator
from welkin.util import model_id


class EncounterDisposition(Resource):
    @model_id("Patient", "Encounter")
    def get(self, patient_id: str, encounter_id: str):
        return super().get(
            f"{self._client.instance}/patients/{patient_id}/encounters/{encounter_id}/disposition"
        )

    @model_id("Patient", "Encounter")
    def update(self, patient_id: str, encounter_id: str, **kwargs):
        return super().patch(
            f"{self._client.instance}/patients/{patient_id}/encounters/{encounter_id}/disposition",
            kwargs,
        )


class EncounterStatus(Enum):
    OPEN = "OPEN"
    CANCELLED = "CANCELLED"
    DRAFT = "DRAFT"
    FINALIZED = "FINALIZED"


class Encounter(Resource):
    subresources = [Assessment, Assessments, EncounterDisposition]
    nested_objects = {
        "assessmentLinks": "Assessments",
        "userRelatedToCalendarEvent": "User",
        "disposition": "EncounterDisposition",
    }

    @model_id("Patient")
    def create(self, patient_id: str):
        return super().post(f"{self._client.instance}/patients/{patient_id}/encounters")

    @model_id("Patient")
    def get(self, patient_id: str, related_data: bool = False):
        encounters = "encounters"
        if related_data:
            encounters = "full-encounters"

        return super().get(
            f"{self._client.instance}/patients/{patient_id}/{encounters}/{self.id}"
        )

    @model_id("Patient")
    def update(self, patient_id: str, **kwargs):
        return super().patch(
            f"{self._client.instance}/patients/{patient_id}/encounters/{self.id}",
            kwargs,
        )

    @model_id("Patient")
    def delete(self, patient_id: str):
        return super().delete(
            f"{self._client.instance}/patients/{patient_id}/encounters/{self.id}"
        )


class Encounters(Collection):
    resource = Encounter
    iterator = MetaInfoIterator

    def get(
        self,
        patient_id: str = None,
        user_id: str = None,
        related_data: bool = None,
        with_care_team: bool = None,
        only_with_calendar_event: bool = None,
        statuses: list = None,
        sort: str = None,
        *args,
        **kwargs,
    ):
        path = f"{self._client.instance}/"
        if patient_id:
            path += f"patients/{patient_id}/"
        elif user_id:
            path += f"users/{user_id}/"
        elif self._parent.__class__.__name__ == "Patient":
            path += f"patients/{self._parent.id}/"
        elif self._parent.__class__.__name__ == "User":
            path += f"users/{self._parent.id}/"

        path += "full-encounters" if related_data else "encounters"

        params = {
            "withCareTeam": with_care_team,
            "statuses": statuses,
            "sort": sort,
            "onlyWithCalendarEvent": only_with_calendar_event,
        }

        return super().get(path, params=params, *args, **kwargs)
