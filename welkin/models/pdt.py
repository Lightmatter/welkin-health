from __future__ import annotations

from welkin.models.base import Collection, Resource
from welkin.pagination import MetaInfoIterator


class PDT(Resource):
    def create(self, pdt_name: str):
        return super().post(f"{self._client.instance}/pdts/{pdt_name}")

    def get(self):
        return super().get(f"{self._client.instance}/pdts/{self.pdtName}/{self.id}")
