from enum import Enum

from welkin.models.base import Collection, Resource


class Assessment(Resource):
    def create(self):
        return super().post(
            f"{self._client.instance}/patients/{self._parent.patientId}/encounters/{self._parent.id}/assessments"
        )

    def get(self):
        return super().get(
            f"{self._client.instance}/patients/{self._parent.patientId}/encounters/{self._parent.id}/assessments/{self.id}"
        )

    def update(self, **kwargs):
        return super().patch(
            f"{self._client.instance}/patients/{self._parent.patientId}/encounters/{self._parent.id}/assessments/{self.id}",
            kwargs,
        )

    def delete(self):
        return super().delete(
            f"{self._client.instance}/patients/{self._parent.patientId}/encounters/{self._parent.id}/assessments/{self.id}"
        )


class Assessments(Collection):
    resource = Assessment

    def get(
        self,
    ):
        path = f"{self._client.instance}/patients/{self._parent.patientId}/encounters/{self._parent.id}/assessments"

        return super().get(path)


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
