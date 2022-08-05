from welkin.models.base import Collection, Resource


class AssessmentRecord(Resource):
    def create(self):
        return super().post(
            f"{self._client.instance}/patients/{self._parent.id}/assessment-records"
        )

    def get(self):
        return super().get(
            f"{self._client.instance}/patients/{self._parent.id}/assessment-records/{self.id}"
        )

    def update_status(self, **kwargs):
        return super().put(
            f"{self._client.instance}/patients/{self._parent.id}/assessment-records/{self.id}",
            kwargs,
        )

    def update_answers(self, **kwargs):
        return super().put(
            f"{self._client.instance}/patients/{self._parent.id}/assessment-records/{self.id}/answers",
            **kwargs,
        )

    def delete(self):
        return super().delete(
            f"{self._client.instance}/patients/{self._parent.id}/assessment-records/{self.id}",
        )


class AssessmentRecords(Collection):
    def get(
        self,
    ):
        path = f"{self._client.instance}/patients/{self._parent.id}/assessment-records"

        return super().get(path)
