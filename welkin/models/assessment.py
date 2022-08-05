from welkin.models.base import Collection, Resource


class AssessmentRecord(Resource):
    def create(self, patient_id: str = None):
        return super().post(
            f"{self._client.instance}/patients/{self.get_patient_id(patient_id)}/assessment-records"
        )

    def get(self, patient_id: str = None):
        return super().get(
            f"{self._client.instance}/patients/{self.get_patient_id(patient_id)}/assessment-records/{self.id}"
        )

    def update_status(self, patient_id: str = None, **kwargs):
        return super().put(
            f"{self._client.instance}/patients/{self.get_patient_id(patient_id)}/assessment-records/{self.id}",
            kwargs,
        )

    def update_answers(self, patient_id: str = None, **kwargs):
        return super().put(
            f"{self._client.instance}/patients/{self.get_patient_id(patient_id)}/assessment-records/{self.id}/answers",
            **kwargs,
        )

    def delete(self, patient_id: str = None):
        return super().delete(
            f"{self._client.instance}/patients/{self.get_patient_id(patient_id)}/assessment-records/{self.id}",
        )

    def get_patient_id(self, patient_id):
        return patient_id if patient_id else self._parent.id


class AssessmentRecords(Collection):
    def get(self, patient_id: str = None, **kwargs):

        if patient_id:
            patientId = patient_id
        else:
            patientId = self._parent.id

        path = f"{self._client.instance}/patients/{patientId}/assessment-records"

        return super().get(path, **kwargs)
