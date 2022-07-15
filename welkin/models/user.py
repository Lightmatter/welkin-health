from enum import Enum

from welkin.models.base import Collection, Resource


class User(Resource):
    def __getattr__(self, name):
        try:
            return super().__getattr__(name)
        except AttributeError as e:
            try:
                sub_resource = self._client.__getattribute__(name)
                sub_resource.user_id = self.id
                return sub_resource
            except AttributeError:
                raise AttributeError(e) from None

    def __str__(self):
        try:
            return f"{self.firstName} {self.lastName}"
        except AttributeError:
            return self.username

    def create(self):
        return super().post("admin/users")

    def get(self):
        return super().get(f"admin/users/{self.id}", params=dict(type="ID"))

    def update(self, **kwargs):
        return super().patch(f"admin/users/{self.username}", kwargs)

    def delete(self):
        return super().delete(f"admin/users/{self.id}", params=dict(type="ID"))


class UserState(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    PROVISIONED = "PROVISIONED"


class Users(Collection):
    resource = User

    def get(
        self,
        search: str = None,
        region: str = None,
        seat_assigned: bool = None,
        user_state: str = None,
    ):
        # TODO: Figure out sort arguments
        params = dict(
            search=search,
            seatAssigned=seat_assigned,
            userState=user_state,
        )

        # User state validation
        if user_state:
            UserState(user_state)

        path = "admin/users"
        if region:
            path = f"{self._client.instance}/users"
            params["region"] = region

        return super().get(path, params=params)
