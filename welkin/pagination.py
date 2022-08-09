class PageIterator:
    def __init__(self, collection, resource, method, size=20, *args, **kwargs):
        self.collection = collection
        self.resource = resource
        self.method = method
        self.size = size
        self.meta_key = None
        self.meta_dict = {"totalPages": 1, "number": 0, "last": True}

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
            self._pre_request()

            self.resources, meta = self.method(
                self.resource,
                meta_key=self.meta_key,
                meta_dict=self.meta_dict,
                *self.args,
                **self.kwargs,
            )

            self._post_request(meta)

            return next(self)

        raise StopIteration

    def _pre_request(self):
        """
        Function to execute before making the next request, e.g. update paging params
        """
        self.kwargs.setdefault("params", {})

    def _post_request(self, meta):
        """
        Function to execute after making the next request, e.g. updating page tracking
        """
        self.last = True

    @property
    def resources(self):
        return self._resources

    @resources.setter
    def resources(self, value):
        self._resources = [self.collection.resource(v) for v in value]
        self.collection.extend(self.resources)


class PageableIterator(PageIterator):
    """
    Most common paging class
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meta_key = "pageable"

    def __iter__(self):
        self.page = 0
        return super().__iter__()

    def _pre_request(self):
        self.kwargs.setdefault("params", {}).update(page=self.page)

    def _post_request(self, meta):
        self.page = meta["number"] + 1
        self.last = meta.get("last")


class PageNumberIterator(PageableIterator):
    """
    PageableIterator with a different key used for the page count
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meta_dict.pop("number")
        self.meta_dict["pageNumber"] = 0

    def _post_request(self, meta):
        self.page = meta["pageNumber"] + 1
        self.last = meta.get("last")


class MetaInfoIterator(PageIterator):
    """
    Functionally identical to PageableIterator with various renamed keys
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meta_key = "metaInfo"
        self.meta_dict.pop("number")
        self.meta_dict["page"] = 0

    def __iter__(self):
        self.page = 0
        return super().__iter__()

    def _pre_request(self):
        self.kwargs.setdefault("params", {}).update(page=self.page)

    def _post_request(self, meta):
        self.page = meta["page"] + 1
        self.last = meta.get("lastPage")


class MetaIterator(PageIterator):
    """
    Paging class for token based paging
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meta_key = "meta"
        self.meta_dict = {
            "nextPageToken": None,
            "prevPageToken": None,
            "pageSize": self.size,
            "found": False,
        }
        self.kwargs.setdefault("params", {}).update(pageSize=self.size)

        if "page_token" in kwargs:
            self.page_token = kwargs["page_token"]

    def __iter__(self):
        self.page_token = None
        return super().__iter__()

    def _pre_request(self):
        if self.page_token:
            self.kwargs["params"] = {"pageToken": self.page_token}

    def _post_request(self, meta):
        self.page_token = meta["nextPageToken"]
        self.last = not meta.get("nextPageToken")
