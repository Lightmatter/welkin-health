from welkin.models.base import Collection, Resource
from welkin.models.pagination import MetaIterator


class Chat(Resource):
    def create(self, patient_id: str):
        return super().post(
            f"{self._client.instance}/patients/{patient_id}/chat/inbound"
        )

    def __str__(self):
        return f"{self.sender['clientType']} {self.message}"


class Chats(Collection):
    resource = Chat
    page_iterator_class = MetaIterator

    def get(
        self,
        patient_id: str,
        pageSize: int = 20,
        includeArchived: bool = False,
        pageToken: str = None,
    ):
        params = {
            "includeArchived": includeArchived,
        }
        # pageToken and pageSize are mutually exclusive
        if pageToken:
            params["pageToken"] = pageToken
        else:
            params["pageSize"] = pageSize

        return super().get(
            f"{self._client.instance}/patients/{patient_id}/chat", params=params
        )


class ChatSearchResult(Resource):
    pass


class SearchChats(Collection):
    resource = ChatSearchResult
    page_iterator_class = MetaIterator

    def get(
        self,
        patient_id: str,
        query: str = None,
        pageToken: str = None,
        pageSize: int = 20,
        contentPageSize: int = 20,
        includeArchived: bool = False,
    ):
        if not query and not pageToken:
            raise Exception('"query" or "pageToken" required.')
        params = {
            "pageSize": pageSize,
            "contentPageSize": contentPageSize,
            "includeArchived": includeArchived,
        }
        if query:
            params["query"] = query
        else:
            params["pageToken"] = pageToken

        return super().get(
            f"{self._client.instance}/patients/{patient_id}/chat/search", params=params
        )
