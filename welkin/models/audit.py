from __future__ import annotations

from welkin.models.base import Collection, Resource
from welkin.pagination import MetaInfoIterator


class WebhookAudit(Resource):
    pass


class WebhookAudits(Collection):
    resource = WebhookAudit
    iterator = MetaInfoIterator

    def get(self, params: dict | None = None, *args, **kwargs):
        if params is None:
            params = {}

        return super().get("admin/audit-webhook", *args, params=params, **kwargs)


class DataAudit(Resource):
    pass


class DataAudits(Collection):
    resource = DataAudit
    iterator = MetaInfoIterator

    def get(self, params: dict | None = None, *args, **kwargs):
        if params is None:
            params = {}

        return super().get("admin/audit-data", *args, params=params, **kwargs)
