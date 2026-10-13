from __future__ import annotations

from welkin.models.base import Collection, Resource
from welkin.pagination import MetaInfoIterator


class Task(Resource):
    def create(self):
        return super().post(f"{self._client.instance}/tasks")

    def get(self):
        return super().get(f"{self._client.instance}/tasks/{self.id}")


class Tasks(Collection):
    resource = Task
    iterator = MetaInfoIterator

    def get(self, *args, **kwargs):
        return super().get(f"{self._client.instance}/tasks", *args, **kwargs)
