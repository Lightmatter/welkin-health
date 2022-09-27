import inspect

from welkin.models import __all__ as all_models


def test_build_resources(client):
    for class_name in all_models:
        assert hasattr(client, class_name)

        attr = getattr(client, class_name)
        assert inspect.isclass(attr)
        assert attr._client == client
