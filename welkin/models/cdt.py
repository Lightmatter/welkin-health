from datetime import datetime

from welkin.models.base import Collection, Resource
from welkin.pagination import PageNumberIterator
from welkin.util import model_id


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
    def get(
        self,
        patient_id: str,
        cdt_name: str,
        fields: list = None,
        filters: dict = None,
        date_start: datetime = None,
        date_end: datetime = None,
        sort: str = None,
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
            params=params,
            *args,
            **kwargs,
        )

    @model_id("Patient")
    def update(self, patient_id: str, cdt_name: str, body: dict = None, **kwargs):
        return super().patch(
            f"{self._client.instance}/patients/{patient_id}/cdts/{cdt_name}",
            json=body,
            **kwargs,
        )
