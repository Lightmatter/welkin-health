import inspect

from welkin.models.base import Collection


def test_collection_get_arguments(client):
    for v in vars(client).values():
        try:
            if issubclass(v, Collection):
                assert hasattr(v, "get"), f"{v} has no get method"

                args = inspect.getfullargspec(v.get)
                assert args.varargs is not None, f"{v}.get must accept variable args"
                assert args.varkw is not None, f"{v}.get must accept variable kwargs"
        except TypeError:
            continue
