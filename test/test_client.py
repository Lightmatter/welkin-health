import inspect

import pytest

from welkin.models import __all__
from welkin.util import Target


@pytest.mark.parametrize("class_name", __all__)
def test_build_resources(client, class_name):
    attr = getattr(client, class_name)

    if issubclass(attr, Target):
        return

    assert inspect.isclass(attr)
    assert attr._client == client
