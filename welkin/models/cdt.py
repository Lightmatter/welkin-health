from __future__ import annotations

from typing import TYPE_CHECKING

from welkin.models.base import Collection, Resource
from welkin.pagination import PageNumberIterator
from welkin.util import model_id

if TYPE_CHECKING:
    from datetime import datetime


class CDT(Resource):
    @model_id("Patient")
    def create(self, patient_id: str):
        return super().post(
            f"{self._client.instance}/patients/{patient_id}/cdts/{self.cdtName}"
        )

    @model_id("Patient")
    def get(self, patient_id: str):
        return super().get(
            f"{self._client.instance}/patients/{patient_id}/cdts/{self.cdtName}/{self.id}"
        )

    @model_id("Patient")
    def update(self, patient_id: str, **kwargs):
        return super().patch(
            f"{self._client.instance}/patients/{patient_id}/cdts/{self.cdtName}/{self.id}",
            kwargs,
        )

    @model_id("Patient")
    def delete(self, patient_id: str):
        return super().delete(
            f"{self._client.instance}/patients/{patient_id}/cdts/{self.cdtName}/{self.id}"
        )


class CDTs(Collection):
    resource = CDT
    iterator = PageNumberIterator

    @model_id("Patient")
    def get(  # noqa: PLR0913
        self,
        patient_id: str,
        cdt_name: str,
        fields: list | None = None,
        filters: dict | None = None,
        date_start: datetime | None = None,
        date_end: datetime | None = None,
        sort: str | None = None,
        *args,
        **kwargs,
    ):
        params = {
            "fields": fields,
            "filters": filters,
            "sort": sort,
            "dateStart": date_start,
            "dateEnd": date_end,
        }

        return super().get(
            f"{self._client.instance}/patients/{patient_id}/cdts/{cdt_name}",
            *args,
            params=params,
            **kwargs,
        )

    @model_id("Patient")
    def update(self, patient_id: str, cdt_name: str, body: dict | None = None, **kwargs):
        return super().patch(
            f"{self._client.instance}/patients/{patient_id}/cdts/{cdt_name}",
            json=body,
            **kwargs,
        )
