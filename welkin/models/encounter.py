from enum import Enum

from welkin.models.assessment import Assessment, Assessments
from welkin.models.base import Collection, Resource
from welkin.models.util import EncounterSubResource, patient_id
from welkin.pagination import MetaInfoIterator


class Disposition(Resource, EncounterSubResource):
    def get(self, patient_id: str = None, encounter_id: str = None):
        patient_id, encounter_id = self.get_patient_encounter_id(
            patient_id, encounter_id
        )
        return super().get(
            f"{self._client.instance}/patients/{patient_id}/encounters/{encounter_id}/disposition"
        )

    def update(self, patient_id: str = None, encounter_id: str = None, **kwargs):
        patient_id, encounter_id = self.get_patient_encounter_id(
            patient_id, encounter_id
        )
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
    subresources = [Assessment, Assessments, Disposition]
    nested_objects = {
        "assessmentLinks": "Assessments",
        "userRelatedToCalendarEvent": "User",
        "disposition": "Disposition",
    }

    @patient_id
    def create(self, patient_id: str = None):
        return super().post(f"{self._client.instance}/patients/{patient_id}/encounters")

    @patient_id
    def get(self, patient_id: str = None, related_data: bool = False):
        encounters = "encounters"
        if related_data:
            encounters = "full-encounters"

        return super().get(
            f"{self._client.instance}/patients/{patient_id}/{encounters}/{self.id}"
        )

    @patient_id
    def update(self, patient_id: str = None, **kwargs):
        return super().patch(
            f"{self._client.instance}/patients/{patient_id}/encounters/{self.id}",
            kwargs,
        )

    @patient_id
    def delete(self, patient_id: str = None):
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
    ):
        root = ""
        if patient_id:
            root = f"patients/{patient_id}"
        elif user_id:
            root = f"users/{user_id}"
        elif self._parent:
            if self._parent.__class__.__name__ == "Patient":
                root = f"patients/{self._parent.id}"
            elif self._parent.__class__.__name__ == "User":
                root = f"users/{self._parent.id}"
        encounters = "encounters"
        if related_data:
            encounters = "full-encounters"

        path = f"{self._client.instance}/{encounters}"
        if root:
            path = f"{self._client.instance}/{root}/{encounters}"

        params = {
            "withCareTeam": with_care_team,
            "statuses": statuses,
            "sort": sort,
            "onlyWithCalendarEvent": only_with_calendar_event,
        }

        return super().get(path, params=params)
