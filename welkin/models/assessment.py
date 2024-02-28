from welkin.models.base import Collection, Resource
from welkin.pagination import PageableIterator
from welkin.util import model_id


class Assessment(Resource):
    @model_id("Patient", "Encounter")
    def create(self, patient_id: str, encounter_id: str):
        return super().post(
            f"{self._client.instance}/patients/{patient_id}/encounters/{encounter_id}"
            "/assessments"
        )

    @model_id("Patient", "Encounter")
    def get(self, patient_id: str, encounter_id: str):
        return super().get(
            f"{self._client.instance}/patients/{patient_id}/encounters/{encounter_id}/"
            f"assessments/{self.id}"
        )

    @model_id("Patient", "Encounter")
    def update(self, patient_id: str, encounter_id: str, **kwargs):
        return super().patch(
            f"{self._client.instance}/patients/{patient_id}/encounters/{encounter_id}/"
            f"assessments/{self.id}",
            kwargs,
        )

    @model_id("Patient", "Encounter")
    def delete(self, patient_id: str, encounter_id: str):
        return super().delete(
            f"{self._client.instance}/patients/{patient_id}/encounters/{encounter_id}/"
            f"assessments/{self.id}"
        )


class Assessments(Collection):
    resource = Assessment
    iterator = PageableIterator

    @model_id("Patient", "Encounter")
    def get(self, patient_id: str, encounter_id: str, *args, **kwargs):
        return super().get(
            f"{self._client.instance}/patients/{patient_id}/encounters/{encounter_id}/"
            "assessments",
            *args,
            **kwargs,
        )


class AssessmentRecordAnswers(Resource):
    @model_id("Patient", "AssessmentRecord")
    def update(self, patient_id: str, assessment_record_id: str):
        return super().put(
            f"{self._client.instance}/patients/{patient_id}/"
            f"assessment-records/{assessment_record_id}/answers"
        )


class AssessmentRecord(Resource):
    subresources = [AssessmentRecordAnswers]

    @model_id("Patient")
    def create(self, patient_id: str):
        return super().post(
            f"{self._client.instance}/patients/{patient_id}/assessment-records"
        )

    @model_id("Patient")
    def get(self, patient_id: str):
        return super().get(
            f"{self._client.instance}/patients/"
            f"{patient_id}/assessment-records/{self.id}"
        )

    @model_id("Patient")
    def update(self, patient_id: str):
        return super().put(
            f"{self._client.instance}/patients/"
            f"{patient_id}/assessment-records/{self.id}"
        )

    @model_id("Patient")
    def delete(self, patient_id: str):
        return super().delete(
            f"{self._client.instance}/patients/"
            f"{patient_id}/assessment-records/{self.id}",
        )


class AssessmentRecords(Collection):
    resource = AssessmentRecord
    iterator = PageableIterator

    @model_id("Patient")
    def get(self, patient_id: str, **kwargs):
        return super().get(
            f"{self._client.instance}/patients/{patient_id}/assessment-records",
            **kwargs,
        )
