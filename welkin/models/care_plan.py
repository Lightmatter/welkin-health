from welkin.models.base import Resource
from welkin.util import model_id


class CarePlanOverview(Resource):
    @model_id("Patient")
    def update(self, patient_id: str):
        return super().put(
            f"{self._client.instance}/patients/{patient_id}/care-plan/overview"
        )


class CarePlan(Resource):
    subresources = [CarePlanOverview]

    @model_id("Patient")
    def create(self, patient_id: str):
        return super().post(
            f"{self._client.instance}/patients/{patient_id}/care-plan/overview"
        )

    @model_id("Patient")
    def get(self, patient_id: str):
        return super().get(f"{self._client.instance}/patients/{patient_id}/care-plan")
