from enum import Enum
from sys import modules

from welkin.models.base import Collection, Resource


class Assessment(Resource):
    def create(self, patient_id: str = None, encounter_id: str = None):
        patientId, encounterId = self.get_patient_encounter_id(patient_id, encounter_id)
        return super().post(
            f"{self._client.instance}/patients/{patientId}/encounters/{encounterId}/assessments"
        )

    def get(self, patient_id: str = None, encounter_id: str = None):
        patientId, encounterId = self.get_patient_encounter_id(patient_id, encounter_id)
        return super().get(
            f"{self._client.instance}/patients/{patientId}/encounters/{encounterId}/assessments/{self.id}"
        )

    def update(self, patient_id: str = None, encounter_id: str = None, **kwargs):
        patientId, encounterId = self.get_patient_encounter_id(patient_id, encounter_id)
        return super().patch(
            f"{self._client.instance}/patients/{patientId}/encounters/{encounterId}/assessments/{self.id}",
            None,
            data=kwargs,
        )

    def delete(self, patient_id: str = None, encounter_id: str = None):
        patientId, encounterId = self.get_patient_encounter_id(patient_id, encounter_id)
        return super().delete(
            f"{self._client.instance}/patients/{patientId}/encounters/{encounterId}/assessments/{self.id}"
        )

    @property
    def patientId(self):
        if isinstance(
            self._parent._parent, getattr(modules["welkin.models"], "Patient")
        ):
            return self._parent._parent.id
        elif hasattr(self._parent, "patientId"):
            return self._parent.patientId
        else:
            # this is the related_data = True case on encounters
            return self._parent.encounter.patientId

    def get_patient_encounter_id(self, patient_id, encounter_id):
        """Helper to retrieve the necessary patient and encounter Ids"""
        if patient_id:
            patientId = patient_id
        else:
            patientId = self.patientId

        if encounter_id:
            encounterId = encounter_id
        else:
            encounterId = self._parent.id

        return patientId, encounterId


class Assessments(Collection):
    resource = Assessment

    def get(self, patient_id: str = None, encounter_id: str = None):

        root = f"{self._client.instance}/patients/"
        if self._parent:
            encounter_id = self._parent.id
            if isinstance(
                self._parent._parent, getattr(modules["welkin.models"], "Patient")
            ):
                patient_id = self._parent._parent.id
            elif hasattr(self._parent, "patientId"):
                patient_id = self._parent.patientId
            else:
                # this is the related_data = True case on encounters
                patient_id = self._parent.encounter.patientId

        path = f"{patient_id}/encounters/{encounter_id}/assessments"

        return super().get(f"{root}{path}")


class EncounterStatus(Enum):
    OPEN = "OPEN"
    CANCELLED = "CANCELLED"
    DRAFT = "DRAFT"
    FINALIZED = "FINALIZED"


class Encounter(Resource):
    subresources = [Assessment, Assessments]
    nested_objects = {
        "assessmentLinks": "Assessments",
        "userRelatedToCalendarEvent": "User",
    }

    def create(self):
        return super().post(
            f"{self._client.instance}/patients/{self._parent.id}/encounters"
        )

    def get(self, related_data: bool = False):
        encounters = "encounters"
        if related_data:
            encounters = "full-encounters"

        return super().get(
            f"{self._client.instance}/patients/{self._parent.id}/{encounters}/{self.id}"
        )

    def update(self, **kwargs):
        return super().patch(
            f"{self._client.instance}/patients/{self._parent.id}/encounters/{self.id}",
            kwargs,
        )

    def delete(self):
        return super().delete(
            f"{self._client.instance}/patients/{self._parent.id}/encounters/{self.id}"
        )


class Encounters(Collection):
    resource = Encounter

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
