from welkin.models.base import Collection, Resource


class Patient(Resource):
    def create(self):
        return super().post(f"{self._client.instance}/patients")

    def get(self):
        return super().get(f"{self._client.instance}/patients")

    def update(self, **kwargs):
        return super().patch(f"{self._client.instance}/patients", kwargs)

    def delete(self):
        raise NotImplementedError("This operation is not supported yet")

    def __str__(self):
        return f"{self.firstName} {self.lastName}"


class Patients(Collection):
    resource = Patient

    def get(self):
        data = {}
        return super().post(f"{self._client.instance}/by-filter/patients", json=data)
