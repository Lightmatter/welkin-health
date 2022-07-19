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
    patientId: str = None
    userId: str = None

    def get(
        self,
        related_data: bool = False,
        *args,
        **kwargs,
    ):
        root = ""
        if self.patientId:
            root = f"patients/{self.patientId}"
        elif self.userId:
            root = f"users/{self.userId}"

        encounters = "encounters"
        if related_data:
            encounters = "full-encounters"

        path = f"{self._client.instance}/{encounters}"
        if root:
            path = f"{self._client.instance}/{root}/{encounters}"

        return super().get(path, *args, **kwargs)
