from welkin.models.base import Collection, Resource
from welkin.pagination import MetaInfoIterator


class CarePlan(Resource):
    def create(self):
        return super().post(
            f"{self._client.instance}/patients/{self._parent.id}/care-plan/overview"
        )

    def get(self):
        return super().get(
            f"{self._client.instance}/patients/{self._parent.id}/care-plan"
        )

    def update(self, **kwargs):
        return super().put(
            f"{self._client.instance}/patients/{self._parent.id}/care-plan/overview",
            kwargs,
        )
