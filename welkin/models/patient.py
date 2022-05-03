from welkin.models.base import Collection, Resource


class Patient(Resource):
    def get(self):
        pass


class Patients(Collection):
    resource = Patient

    def get(self):
        data = {}
        return super().post(f"{self._instance}/by-filter/patients", json=data)
