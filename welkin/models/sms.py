from welkin.models.base import Collection, Resource
from welkin.pagination import PageableIterator
from welkin.util import model_id


class SMS(Resource):
    @model_id("Patient")
    def get(self, patient_id: str, *args, **kwargs):
        return super().get(
            f"{self._client.instance}/patients/{patient_id}/sms/{self.id}",
            *args,
            **kwargs,
        )


class SMSes(Collection):
    resource = SMS
    iterator = PageableIterator

    @model_id("Patient")
    def get(self, patient_id: str, sort: str = None, *args, **kwargs):
        params = {
            "sort": sort,
        }

        return super().get(
            f"{self._client.instance}/patients/{patient_id}/sms",
            params=params,
            *args,
            **kwargs,
        )
