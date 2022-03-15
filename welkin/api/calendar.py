from welkin.api.schema import Resource


class Calendar(Resource):
    def get(self):
        return super().get("calendar")
