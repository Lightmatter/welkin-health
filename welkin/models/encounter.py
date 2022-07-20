from welkin.models.base import Collection, Resource


class Encounter(Resource):
    def create(self):
        return super().post(
            f"{self._client.instance}/patients/{self.patientId}/encounters"
        )

    def get(self, related_data: bool = False):
        encounters = "encounters"
        if related_data:
            encounters = "full-encounters"

        return super().get(
            f"{self._client.instance}/patients/{self.patientId}/{encounters}/{self.id}"
        )

    def update(self, **kwargs):
        return super().patch(
            f"{self._client.instance}/patients/{self.patientId}/encounters/{self.id}",
            kwargs,
        )

    def delete(self):
        return super().delete(
            f"{self._client.instance}/patients/{self.patientId}/encounters/{self.id}"
        )


class Encounters(Collection):
    resource = Encounter

    def get(
        self,
        patient_id: str = None,
        user_id: str = None,
        related_data: bool = False,
        *args,
        **kwargs,
    ):
        root = ""
        if patient_id:
            root = f"patients/{patient_id}"
        elif user_id:
            root = f"users/{user_id}"
        elif self._parent:
            if self._parent.__class__.__name__ == "Patient":
                f"patients/{self._parent.id}"
            elif self._parent.__class__.__name__ == "User":
                f"users/{self._parent.id}"
        encounters = "encounters"
        if related_data:
            encounters = "full-encounters"

        path = f"{self._client.instance}/{encounters}"
        if root:
            path = f"{self._client.instance}/{root}/{encounters}"

        return super().get(path, *args, **kwargs)
