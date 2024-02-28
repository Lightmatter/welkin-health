import inspect

import pytest

from welkin.models import Patient, __all__
from welkin.models.base import Collection
from welkin.pagination import PageIterator


@pytest.mark.parametrize("class_name", __all__)
def test_collection_pageable(client, class_name: str):
    cls = getattr(client, class_name)
    if not issubclass(cls, Collection):
        return

    assert hasattr(cls, "get"), f"{cls} has no get method"
    assert issubclass(cls.iterator, PageIterator)

    method = cls.get
    args = inspect.getfullargspec(method)
    assert args.varargs is not None, f"{method} must accept variable args"
    assert args.varkw is not None, f"{method} must accept variable kwargs"


@pytest.mark.parametrize("class_name", __all__)
def test_method_args(client, class_name: str):
    cls = getattr(client, class_name)

    for method_name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        if method_name.startswith("__"):
            continue  # skip dunder methods

        if hasattr(method, "__wrapped__"):
            method = method.__wrapped__  # unwrap decorated functions

        if method.__qualname__ != f"{class_name}.{method_name}":
            continue  # skip methods from parent classes

        args = inspect.getfullargspec(method)

        if cls in Patient.subresources:
            try:
                assert args.args.index("patient_id") == 1, "patient_id must be first"
            except ValueError:
                pytest.fail(f"{method} must accept patient_id")
