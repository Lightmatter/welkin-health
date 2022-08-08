from welkin.models.base import Collection, Resource


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


def patient_id(func):
    def wrapper(cls, *args, **kwargs):
        if "patient_id" not in kwargs:
            try:
                kwargs["patient_id"] = cls._parent.id
            except AttributeError:
                raise TypeError(
                    f"{func.__name__} is missing 1 required positional argument: "
                    "'patient_id"
                ) from None

        return func(cls, *args, **kwargs)

    return wrapper


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

    @patient_id
    def get(self, patient_id: str = None, **kwargs):
        path = f"{self._client.instance}/patients/{patient_id}/assessment-records"

        return super().get(path, **kwargs)
