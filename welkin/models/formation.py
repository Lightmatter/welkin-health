from welkin.models.base import Collection, Resource
from welkin.pagination import PageableIterator


class Formations(Collection):
    iterator = PageableIterator

    def get(self, data_type: str, version: str = "current"):
        return super().get(f"{self._client.instance}/formations/{version}/{data_type}")
