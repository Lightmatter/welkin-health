from sys import modules

from welkin.models.base import Collection, Resource
from welkin.models.util import EncounterSubResource, patient_id
from welkin.pagination import PageableIterator


class Assessment(Resource, EncounterSubResource):
    def create(self, patient_id: str = None, encounter_id: str = None):
        patient_id, encounter_id = self.get_patient_encounter_id(
            patient_id, encounter_id
        )
        return super().post(
            f"{self._client.instance}/patients/{patient_id}/encounters/{encounter_id}"
            "/assessments"
        )

    def get(self, patient_id: str = None, encounter_id: str = None):
        patient_id, encounter_id = self.get_patient_encounter_id(
            patient_id, encounter_id
        )
        return super().get(
            f"{self._client.instance}/patients/{patient_id}/encounters/{encounter_id}/"
            f"assessments/{self.id}"
        )

    def update(self, patient_id: str = None, encounter_id: str = None, **kwargs):
        patient_id, encounter_id = self.get_patient_encounter_id(
            patient_id, encounter_id
        )
        return super().patch(
            f"{self._client.instance}/patients/{patient_id}/encounters/{encounter_id}/"
            f"assessments/{self.id}",
            kwargs,
        )

    def delete(self, patient_id: str = None, encounter_id: str = None):
        patient_id, encounter_id = self.get_patient_encounter_id(
            patient_id, encounter_id
        )
        return super().delete(
            f"{self._client.instance}/patients/{patient_id}/encounters/{encounter_id}/"
            f"assessments/{self.id}"
        )


class Assessments(Collection):
    resource = Assessment
    iterator = PageableIterator

    def get(self, patient_id: str = None, encounter_id: str = None, *args, **kwargs):
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

        return super().get(f"{root}{path}", *args, **kwargs)


class AssessmentRecordAnswers(Resource):
    def update(self, patient_id: str = None, assessment_record_id: str = None):
        if not assessment_record_id:
            assessment_record_id = self._parent.id

        if not patient_id:
            patient_id = self._parent.get_patient_id(patient_id)

        return super().put(
            f"{self._client.instance}/patients/{patient_id}/"
            f"assessment-records/{assessment_record_id}/answers"
        )


class AssessmentRecord(Resource):
    subresources = [AssessmentRecordAnswers]

    @patient_id
    def create(self, patient_id: str = None):
        return super().post(
            f"{self._client.instance}/patients/{patient_id}/assessment-records"
        )

    @patient_id
    def get(self, patient_id: str = None):
        return super().get(
            f"{self._client.instance}/patients/"
            f"{patient_id}/assessment-records/{self.id}"
        )

    @patient_id
    def update(self, patient_id: str = None):
        return super().put(
            f"{self._client.instance}/patients/"
            f"{patient_id}/assessment-records/{self.id}"
        )

    @patient_id
    def delete(self, patient_id: str = None):
        return super().delete(
            f"{self._client.instance}/patients/"
            f"{patient_id}/assessment-records/{self.id}",
        )

    def get_patient_id(self, patient_id):
        return patient_id if patient_id else self._parent.id


class AssessmentRecords(Collection):
    resource = AssessmentRecord
    iterator = PageableIterator

    @patient_id
    def get(self, patient_id: str = None, **kwargs):
        path = f"{self._client.instance}/patients/{patient_id}/assessment-records"

        return super().get(path, **kwargs)
