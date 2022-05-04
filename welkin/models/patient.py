from welkin.models.base import Collection, Resource


class Patient(Resource):
    def get(self):
        return super().get(f"{self._instance}/patients")

    def __str__(self):
        return f"{self.firstName} {self.lastName}"


class Patients(Collection):
    resource = Patient

    def get(self):
        data = {}
        return super().post(f"{self._instance}/by-filter/patients", json=data)
