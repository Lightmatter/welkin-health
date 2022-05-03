from welkin.api.schema import Resource


class Patients(Resource):
    def get(self):
        data = {}
        response = self._client.post("by-filter/patients", json=data)

        return response
