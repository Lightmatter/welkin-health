from welkin.models.base import PageIterator


class PageableIterator(PageIterator):
    """
    Most common paging class
    """

    def __init__(self, collection, resource, method, size=20, *args, **kwargs):
        super().__init__(collection, resource, method, size, *args, **kwargs)
        self.meta_key = "pageable"
        self.meta_dict.pop("page")
        self.meta_dict["number"] = 0

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

    def __init__(self, collection, resource, method, size=20, *args, **kwargs):
        super().__init__(collection, resource, method, size, *args, **kwargs)
        self.meta_dict.pop("number")
        self.meta_dict["pageNumber"] = 0

    def _post_request(self, meta):
        self.page = meta["pageNumber"] + 1
        self.last = meta.get("last")


class MetaInfoIterator(PageIterator):
    """
    Functionally identical to PageableIterator with various renamed keys
    """

    def __init__(self, collection, resource, method, size=20, *args, **kwargs):
        super().__init__(collection, resource, method, size, *args, **kwargs)
        self.meta_key = "metaInfo"

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

    def __init__(self, collection, resource, method, size=20, *args, **kwargs):
        super().__init__(collection, resource, method, size, *args, **kwargs)
        self.meta_key = "meta"
        self.meta_dict = {
            "nextPageToken": None,
            "prevPageToken": None,
            "pageSize": 20,
            "found": False,
        }

    def __iter__(self):
        self.pageToken = None
        return super().__iter__()

    def _pre_request(self):
        self.kwargs.setdefault("params", {}).update(pageToken=self.pageToken)

    def _post_request(self, meta):
        self.pageToken = meta["nextPageToken"]
        self.last = not meta.get("nextPageToken")
