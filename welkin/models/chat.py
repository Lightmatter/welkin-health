from welkin.models.base import Collection, Resource
from welkin.pagination import MetaIterator
from welkin.util import model_id


class Chat(Resource):
    @model_id("Patient")
    def create(self, patient_id: str):
        return super().post(
            f"{self._client.instance}/patients/{patient_id}/chat/inbound"
        )

    def __str__(self):
        return f"{self.sender['clientType']} {self.message}"


class Chats(Collection):
    resource = Chat
    iterator = MetaIterator

    @model_id("Patient")
    def get(self, patient_id: str, include_archived: bool = False, *args, **kwargs):
        params = {
            "includeArchived": include_archived,
        }

        return super().get(
            f"{self._client.instance}/patients/{patient_id}/chat",
            params=params,
            *args,
            **kwargs,
        )


class ChatSearchResult(Resource):
    pass


class SearchChats(Collection):
    resource = ChatSearchResult
    iterator = MetaIterator

    @model_id("Patient")
    def get(
        self,
        patient_id: str,
        query: str,
        content_page_size: int = 20,
        include_archived: bool = False,
        *args,
        **kwargs,
    ):
        params = {
            "query": query,
            "contentPageSize": content_page_size,
            "includeArchived": include_archived,
        }

        return super().get(
            f"{self._client.instance}/patients/{patient_id}/chat/search",
            params=params,
            *args,
            **kwargs,
        )
