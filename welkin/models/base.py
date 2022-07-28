import sys


class SchemaBase:
    _client = None
    _parent = None
    subresources = []

    def __getattr__(self, name):
        try:
            for r in self.subresources:
                if r.__name__ == name:
                    r._parent = self
                    return r

        except AttributeError:
            pass

        try:
            return super().__getattribute__(name)
        except AttributeError as e:
            raise AttributeError(e) from None


class Resource(dict, SchemaBase):
    nested_objects = {}

    def __getattr__(self, name):
        try:
            value = super().__getitem__(name)
        except KeyError:
            value = super().__getattr__(name)

        if name in self.nested_objects:
            cls = getattr(sys.modules["welkin.models"], self.nested_objects[name])
            if issubclass(cls, Collection):
                value = cls(cls.resource(item) for item in value)
            else:
                value = cls(value)

        return value

    def __setattr__(self, name, value):
        super().__setitem__(name, value)

    def __str__(self):
        id = getattr(self, "id", "")

        return f"{self.__class__.__name__} #{id}" if id else self.__class__.__name__

    def __repr__(self):
        return object.__repr__(self)

    def get(self, resource, subresource=None, *args, **kwargs):
        response = self._client.get([resource, subresource], *args, **kwargs)
        super().update(response)

        return self

    def patch(self, resource, data, *args, **kwargs):
        response = self._client.patch(
            resource,
            json=data,
            *args,
            **kwargs,
        )

        super().update(response)

        return self

    def post(self, resource, *args, **kwargs):
        response = self._client.post(
            resource,
            json=self,
            *args,
            **kwargs,
        )
        super().update(response)

        return self

    def put(self, resource, *args, **kwargs):
        response = self._client.put(
            resource,
            json=self,
            *args,
            **kwargs,
        )

        super().update(response)

        return self

    def delete(self, resource, *args, **kwargs):
        response = self._client.delete(resource, *args, **kwargs)
        super().update(response)

        return self


class PageIterator:
    def __init__(self, collection, resource, method, size=20, *args, **kwargs):
        self.collection = collection
        self.resource = resource
        self.method = method
        self.size = size

        if size != 20:
            kwargs.setdefault("params", {}).update(size=size)

        self.args = args
        self.kwargs = kwargs

    def __iter__(self):
        self._resources = []
        self.last = False

        return self

    def __next__(self):
        if self.resources:
            return self.resources.pop(0)

        if not self.last:
            self.kwargs.setdefault("params", {}).update(page=self.page)
            results = self.method(
                self.resource,
                meta_key=self._get_meta_key(),
                meta_dict=self._get_meta_dict(),
                *self.args,
                **self.kwargs,
            )
            self.resources, meta = results

            self._set_page(meta)

            self._set_last(meta)

            return next(self)

        raise StopIteration

    def _get_meta_key(self):
        """
        json.pop("pageable", {}) or json.pop("metaInfo", {}) or json.pop("meta", {})
        """
        return None

    def _get_meta_dict(self):
        return {"totalPages": 1, "page": 0, "last": True}

    def _set_page(self, meta):
        self.page = 1

    def _set_last(self, meta):
        # meta.get("last") or meta.get("lastPage") or not meta.get("nextPageToken")
        self.last = True

    @property
    def resources(self):
        return self._resources

    @resources.setter
    def resources(self, value):
        self._resources = [self.collection.resource(v) for v in value]
        self.collection.extend(self.resources)


class Collection(list, SchemaBase):
    resource = Resource
    page_iterator_class = PageIterator

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.__class__(*super().__getitem__(index))

        return super().__getitem__(index)

    def __str__(self):
        return str([str(i) for i in self])

    def __repr__(self):
        return object.__repr__(self)

    def get(self, *args, **kwargs):
        return self.request(self._client.get, *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.request(self._client.post, *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.request(self._client.patch, *args, **kwargs)

    def request(self, method, resource, paginate=False, *args, **kwargs):
        paginator = self.page_iterator_class(self, resource, method, *args, **kwargs)

        if paginate:
            return paginator

        self.clear()
        for n, _ in enumerate(paginator):
            if n == paginator.size - 1:
                break

        return self


class PageableIterator(PageIterator):
    def __iter__(self):
        self.page = 0
        return super().__iter__()

    def _get_meta_key(self):
        return "pageable"

    def _set_page(self, meta):
        self.page = meta["number"] + 1

    def _set_last(self, meta):
        self.last = meta.get("last")


class MetaInfoIterator(PageIterator):
    def __iter__(self):
        self.page = 0
        return super().__iter__()

    def _get_meta_key(self):
        return "metaInfo"

    def _set_page(self, meta):
        self.page = meta["page"] + 1

    def _set_last(self, meta):
        self.last = meta.get("lastPage")


class MetaIterator(PageIterator):
    def _get_meta_key(self):
        return "meta"

    def _get_meta_dict(self):
        return {
            "nextPageToken": None,
            "prevPageToken": None,
            "pageSize": 20,
            "found": False,
        }

    def _set_page(self, meta):
        """
        As this pagniation style is token based, page will not be included
        """
        return

    def _set_last(self, meta):
        self.last = not meta.get("nextPageToken")
