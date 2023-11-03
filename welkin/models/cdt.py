from datetime import datetime

from welkin.models.base import Collection, Resource
from welkin.pagination import PageNumberIterator


class CDT(Resource):
    def create(self):
        return super().post(
            f"{self._client.instance}/patients/{self._parent.id}/cdts/{self.cdtName}"
        )

    def get(self):
        return super().get(
            f"{self._client.instance}/patients/{self._parent.id}/cdts/{self.cdtName}/{self.id}"
        )

    def update(self, **kwargs):
        return super().patch(
            f"{self._client.instance}/patients/{self._parent.id}/cdts/{self.cdtName}/{self.id}",
            kwargs,
        )

    def delete(self):
        return super().delete(
            f"{self._client.instance}/patients/{self._parent.id}/cdts/{self.cdtName}/{self.id}"
        )


class CDTs(Collection):
    resource = CDT
    iterator = PageNumberIterator

    def get(
        self,
        patient_id: str = None,
        cdt_name: str = None,
        fields: list = None,
        filters: dict = None,
        date_start: datetime = None,
        date_end: datetime = None,
        sort: str = None,
        *args,
        **kwargs,
    ):
        root = ""
        if patient_id:
            root = f"patients/{patient_id}"
        else:
            root = f"patients/{self._parent.id}"

        cdt_path = ""
        if cdt_name:
            cdt_path = f"cdts/{cdt_name}"

        path = f"{self._client.instance}/{root}/{cdt_path}"

        params = {
            "fields": fields,
            "filters": filters,
            "sort": sort,
            "dateStart": date_start,
            "dateEnd": date_end,
        }

        return super().get(path, params=params, *args, **kwargs)

    def update(
        self, patient_id: str = None, cdt_name: str = None, body: dict = None, **kwargs
    ):
        root = ""
        if patient_id:
            root = f"patients/{patient_id}"
        else:
            root = f"patients/{self._parent.id}"

        cdt_path = ""
        if cdt_name:
            cdt_path = f"cdts/{cdt_name}"

        path = f"{self._client.instance}/{root}/{cdt_path}"

        return super().patch(path, json=body, **kwargs)
