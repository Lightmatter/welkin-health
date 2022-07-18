from welkin.models.base import Collection, Resource


class Assessment(Resource):
    def create(self):
        return super().post(
            f"{self._client.instance}/patients/{self.patient_id}/encounters/{self.encounter_id}/assessments"
        )

    def get(self):
        return super().get(
            f"{self._client.instance}/patients/{self.patient_id}/encounters/{self.encounter_id}/assessments/{self.id}"
        )

    def update(self, **kwargs):
        return super().patch(
            f"{self._client.instance}/patients/{self.patient_id}/encounters/{self.encounter_id}/assessments/{self.id}",
            kwargs,
        )

    def delete(self):
        return super().delete(
            f"{self._client.instance}/patients/{self.patientId}/encounters/{self.encounterId}/assessments/{self.id}"
        )


class Assessments(Collection):
    resource = Assessment
    encounter_id: str = None
    patient_id: str = None

    def __init__(self, encounter_id=None, patient_id=None):
        self.encounter_id = encounter_id
        self.patient_id = patient_id

    def get(
        self,
        patient_id: str,
        encounter_id: str,
        *args,
        **kwargs,
    ):

        return super().get(
            f"{self._client.instance}/patients/{patient_id}/encounters/{encounter_id}/assessments",
            *args,
            **kwargs,
        )


class Comment(Resource):
    def create(self):
        return super().post(
            f"{self._client.instance}/patients/{self.patient_id}/encounters/{self.encounter_id}/comments"
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
    encounter_id: str = None
    patient_id: str = None

    def __init__(self, encounter_id=None, patient_id=None):
        self.encounter_id = encounter_id
        self.patient_id = patient_id

    def get(
        self,
        *args,
        **kwargs,
    ):

        return super().get(
            f"{self._client.instance}/patients/{self.patient_id}/encounters/{self.encounter_id}/comments",
            *args,
            **kwargs,
        )


class Disposition(Resource):
    def get(self):
        return super().get(
            f"{self._client.instance}/patients/{self.patient_id}/encounters/{self.encounter_id}/disposition"
        )


class Encounter(Resource):
    sub_resources = [Comments, Disposition]

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

    @property
    def Comments(self):
        return self._client.Comments(encounter_id=self.id, patient_id=self.patient_id)

    @property
    def Disposition(self):
        return self._client.Disposition(
            encounter_id=self.id, patient_id=self.patient_id
        )


class Encounters(Collection):
    resource = Encounter
    patient_id: str = None
    user_id: str = None

    def __init__(self, patient_id=None, user_id=None):
        self.patient_id = patient_id
        self.user_id = user_id

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
