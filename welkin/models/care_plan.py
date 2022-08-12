from welkin.models.base import Resource
from welkin.models.util import find_patient_id_in_parents


class CarePlanOverview(Resource):
    def update(self, patient_id: str = None):
        if not patient_id:
            # self._parent -> CarePlan
            # CarePlan._parent -> Patient
            patient_id = find_patient_id_in_parents(self)
        return super().put(
            f"{self._client.instance}/patients/{patient_id}/care-plan/overview"
        )


class CarePlan(Resource):
    subresources = [CarePlanOverview]

    def create(self, patient_id: str = None):
        if not patient_id:
            # self._parent -> Patient
            patient_id = find_patient_id_in_parents(self)
        return super().post(
            f"{self._client.instance}/patients/{patient_id}/care-plan/overview"
        )

    def get(self, patient_id: str = None):
        if not patient_id:
            # self._parent -> Patient
            patient_id = find_patient_id_in_parents(self)
        return super().get(f"{self._client.instance}/patients/{patient_id}/care-plan")
