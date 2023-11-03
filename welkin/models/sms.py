from welkin.models.base import Collection, Resource
from welkin.models.util import patient_id
from welkin.pagination import PageableIterator


class SMS(Resource):
    @patient_id
    def get(self, patient_id: str = None, *args, **kwargs):
        return super().get(
            f"{self._client.instance}/patients/{patient_id}/sms/{self.id}",
            *args,
            **kwargs,
        )


class SMSes(Collection):
    resource = SMS
    iterator = PageableIterator

    @patient_id
    def get(self, patient_id: str = None, sort: str = None, *args, **kwargs):
        params = {
            "sort": sort,
        }

        return super().get(
            f"{self._client.instance}/patients/{patient_id}/sms",
            params=params,
            *args,
            **kwargs,
        )
