from welkin.models.base import Collection, Resource


class AssessmentRecordAnswers(Resource):
    def update(self, patient_id: str = None, assessment_record_id: str = None):
        if isinstance(self._parent, AssessmentRecord):
            assessmentRecordId = self._parent.id
            patientId = self._parent.get_patient_id(patient_id)
        else:
            assessmentRecordId = assessment_record_id
            patientId = patient_id

        return super().put(
            f"{self._client.instance}/patients/{patientId}/assessment-records/{assessmentRecordId}/answers"
        )


class AssessmentRecordStatus(Resource):
    def update(self, patient_id: str = None, assessment_record_id: str = None):
        if isinstance(self._parent, AssessmentRecord):
            assessmentRecordId = self._parent.id
            patientId = self._parent.get_patient_id(patient_id)
        else:
            assessmentRecordId = assessment_record_id
            patientId = patient_id

        return super().put(
            f"{self._client.instance}/patients/{patientId}/assessment-records/{assessmentRecordId}"
        )


class AssessmentRecord(Resource):
    subresources = [AssessmentRecordAnswers]

    def create(self, patient_id: str = None):
        return super().post(
            f"{self._client.instance}/patients/{self.get_patient_id(patient_id)}/assessment-records"
        )

    def get(self, patient_id: str = None):
        return super().get(
            f"{self._client.instance}/patients/{self.get_patient_id(patient_id)}/assessment-records/{self.id}"
        )

    def update(self, patient_id: str = None):
        return super().get(
            f"{self._client.instance}/patients/{self.get_patient_id(patient_id)}/assessment-records/{self.id}"
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
