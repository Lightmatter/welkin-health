from __future__ import annotations

from welkin.models.base import Resource


class Contact(Resource):
    def create(self, patient_id: str):
        return super().post(f"{self._client.instance}/patients/{patient_id}/contacts")
