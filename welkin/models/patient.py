from welkin.models.base import Collection, Resource


class Patient(Resource):
    def __getattr__(self, name):
        try:
            return super().__getattr__(name)
        except AttributeError as e:
            try:
                sub_resource = self._client.__getattribute__(name)
                sub_resource.patient_id = self.id
                return sub_resource
            except AttributeError:
                raise AttributeError(e) from None

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


class Patients(Collection):
    resource = Patient

    def get(self, filter={}, *args, **kwargs):
        # TODO: Add sort and query arguments.
        return super().post(
            f"{self._client.instance}/by-filter/patients", json=filter, *args, **kwargs
        )
