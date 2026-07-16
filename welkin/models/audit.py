from welkin.models.base import Collection, Resource
from welkin.pagination import MetaInfoIterator


class Audit(Resource):
    pass


class Audits(Collection):
    resource = Audit
    iterator = MetaInfoIterator

    def get(self, **kwargs):
        return super().get("admin/audit-webhook", params=kwargs)
