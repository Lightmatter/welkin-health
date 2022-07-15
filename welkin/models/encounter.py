from attr import Attribute

from welkin.models.base import Collection, Resource
from welkin.models.patient import Patient


class Encounter(Resource):
    def create(self):
        return super().post(
            f"{self._client.instance}/patients/{self.patient_id}/encounters"
        )

    def get(self, related_data: bool = False):
        encounters = "encounters"
        if related_data:
            encounters = "full-encounters"

        return super().get(
            f"{self._client.instance}/patients/{self.patient_id}/{encounters}/{self.id}"
        )

    def update(self, **kwargs):
        return super().patch(
            f"{self._client.instance}/patients/{self.patient_id}/encounters", kwargs
        )

    def delete(self):
        return super().delete(
            f"{self._client.instance}/patients/{self.patient_id}/encounters/{self.id}"
        )


class Encounters(Collection):
    resource = Encounter

    def get(
        self,
        related_data: bool = False,
        *args,
        **kwargs,
    ):
        root = ""
        if self.patient_id:
            root = f"patients/{self.patient_id}"
        elif self.user_id:
            root = f"users/{self.user_id}"

        encounters = "encounters"
        if related_data:
            encounters = "full-encounters"

        path = f"{self._client.instance}/{encounters}"
        if root:
            path = f"{self._client.instance}/{root}/{encounters}"

        return super().get(path, *args, **kwargs)


class Comment(Resource):
    def create(self):
        return super().post(
            f"{self._client.instance}/patients/{self.patient_id}/encounters"
        )

    def get(self):

        return super().get(
            f"{self._client.instance}/patients/{self.patient_id}/encounters/{self.encounter_id}/comments/{self.id}"
        )

    def update(self, **kwargs):
        return super().put(
            f"{self._client.instance}/patients/{self.patient_id}/encounters/{self.encounter_id}/comments/{self.id}",
            kwargs,
        )

    def delete(self):
        return super().delete(
            f"{self._client.instance}/patients/{self.patientId}/encounters/{self.encounterId}/comments/{self.id}"
        )


class Comments(Collection):
    resource = Comment

    def get(
        self,
        patient_id: str,
        encounter_id: str,
        *args,
        **kwargs,
    ):

        return super().get(
            f"{self._client.instance}/patients/{patient_id}/encounters/{encounter_id}/comments",
            *args,
            **kwargs,
        )


class Disposition(Encounter, Resource):
    def get(self):
        return super().get(
            f"{self._client.instance}/patients/{self.patient_id}/encounters/{self.encounter_id}/disposition"
        )
