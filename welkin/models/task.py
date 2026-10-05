from __future__ import annotations

from welkin.models.base import Resource


class Task(Resource):
    def create(self):
        return super().post(f"{self._client.instance}/tasks")
