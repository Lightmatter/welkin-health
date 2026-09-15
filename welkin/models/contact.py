from __future__ import annotations

from welkin.models.base import Resource
from welkin.util import model_id


class Contact(Resource):
    @model_id("Patient")
    def create(self, patient_id: str):
        return super().post(f"{self._client.instance}/patients/{patient_id}/contacts")
