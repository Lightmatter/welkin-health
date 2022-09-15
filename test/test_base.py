import inspect

from welkin.models.base import Collection
from welkin.pagination import PageIterator


def test_collection_pageable(client):
    for v in vars(client).values():
        try:
            if not issubclass(v, Collection):
                continue
        except TypeError:
            continue

        assert hasattr(v, "get"), f"{v} has no get method"
        assert issubclass(v.iterator, PageIterator)

        args = inspect.getfullargspec(v.get)
        assert args.varargs is not None, f"{v}.get must accept variable args"
        assert args.varkw is not None, f"{v}.get must accept variable kwargs"
