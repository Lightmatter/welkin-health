from welkin.models.base import Resource


class CarePlanOverview(Resource):
    def update(self):
        return super().put(
            f"{self._client.instance}/patients/{self._parent._parent.id}/care-plan/overview"
        )


class CarePlan(Resource):
    subresources = [CarePlanOverview]

    def create(self):
        return super().post(
            f"{self._client.instance}/patients/{self._parent.id}/care-plan/overview"
        )

    def get(self):
        return super().get(
            f"{self._client.instance}/patients/{self._parent.id}/care-plan"
        )
