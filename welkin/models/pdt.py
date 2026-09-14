from __future__ import annotations

from welkin.models.base import Collection, Resource
from welkin.pagination import MetaInfoIterator


class PDT(Resource):
    def create(self, pdt_name: str):
        return super().post(f"{self._client.instance}/pdts/{pdt_name}")

    def get(self):
        return super().get(f"{self._client.instance}/pdts/{self.pdtName}/{self.id}")

    def update(self, **kwargs):
        return super().patch(
            f"{self._client.instance}/pdts/{self.pdtName}/{self.id}", kwargs
        )

    def delete(self):
        return super().delete(f"{self._client.instance}/pdts/{self.pdtName}/{self.id}")


class PDTs(Collection):
    resource = PDT
    iterator = MetaInfoIterator

    def get(self, pdt_name: str, *args, **kwargs):
        return super().get(f"{self._client.instance}/pdts/{pdt_name}", *args, **kwargs)
