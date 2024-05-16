from __future__ import annotations

from welkin.models.base import Collection, Resource
from welkin.models.encounter import Encounters
from welkin.pagination import CursorIterator


class CDTRecordExport(Resource):
    subresources = (Encounters,)

    def __str__(self):
        try:
            return f"{self.firstName} {self.lastName}"
        except AttributeError:
            return self.username


class CDTRecordsExport(Collection):
    resource = CDTRecordExport
    iterator = CursorIterator

    def get(self, *args, **kwargs):
        return super().get(f"{self._client.instance}/export/CDT_RECORD", *args, **kwargs)
