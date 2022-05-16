from welkin.models.base import Collection, Resource


class User(Resource):
    def __str__(self):
        return f"{self.firstName} {self.lastName}"

    def create(self):
        return super().post("admin/users")

    def get(self):
        return super().get(f"admin/users/{self.id}", params=dict(type="ID"))

    def update(self, **kwargs):
        return super().patch(f"admin/users/{self.username}", kwargs)

    def delete(self):
        return super().delete(f"admin/users/{self.id}", params=dict(type="ID"))


class Users(Collection):
    resource = User

    def get(self, *args, **kwargs):
        # TODO: Add sort and query arguments.
        return super().get("admin/users", *args, **kwargs)

    def search(self, search):
        return self.get(params=dict(search=search))
