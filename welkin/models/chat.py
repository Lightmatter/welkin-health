from welkin.models.base import Collection, Resource
from welkin.pagination import MetaIterator


class Chat(Resource):
    def create(self):
        return super().post(
            f"{self._client.instance}/patients/{self._parent.id}/chat/inbound"
        )

    def __str__(self):
        return f"{self.sender['clientType']} {self.message}"


class Chats(Collection):
    resource = Chat
    iterator = MetaIterator

    def get(self, include_archived: bool = False, **kwargs):
        params = {
            "includeArchived": include_archived,
        }

        return super().get(
            f"{self._client.instance}/patients/{self._parent.id}/chat",
            params=params,
            **kwargs,
        )


class ChatSearchResult(Resource):
    pass


class SearchChats(Collection):
    resource = ChatSearchResult
    iterator = MetaIterator

    def get(
        self,
        query: str,
        content_page_size: int = 20,
        include_archived: bool = False,
        **kwargs,
    ):
        params = {
            "query": query,
            "contentPageSize": content_page_size,
            "includeArchived": include_archived,
        }

        return super().get(
            f"{self._client.instance}/patients/{self._parent.id}/chat/search",
            params=params,
            **kwargs,
        )
