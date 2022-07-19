from welkin.models.base import Collection, Resource
from welkin.models.encounter import Encounter, Encounters


class Patient(Resource):
    sub_resources = [Encounter, Encounters]

    def create(self):
        return super().post(f"{self._client.instance}/patients")

    def get(self):
        return super().get(f"{self._client.instance}/patients/{self.id}")

    def update(self, **kwargs):
        return super().patch(f"{self._client.instance}/patients/{self.id}", kwargs)

    def delete(self):
        return super().delete(f"{self._client.instance}/patients/{self.id}")

    def __str__(self):
        return f"{self.firstName} {self.lastName}"

    def Encounters(self):
        encounters = self._client.Encounters()
        encounters.patientId = self.id
        return encounters

    def Encounter(self, **kwargs):
        return self._client.Encounter(patientId=self.id, **kwargs)


class Patients(Collection):
    resource = Patient

    def get(self, filter={}, *args, **kwargs):
        # TODO: Add sort and query arguments.
        return super().post(
            f"{self._client.instance}/by-filter/patients", json=filter, *args, **kwargs
        )
