from datetime import date, datetime, timezone
from functools import lru_cache, wraps
from typing import Any, Callable, Tuple, Union
from uuid import UUID

import inflection

from welkin.models.base import Collection, Resource, SchemaBase

# NOTE: `clean_request_payload` and `clean_request_params` are intentionally DRY
# violations. The code may be the same, but they represent different knowledge.
# the same goes for `clean_request_payload` and `clean_json_list`


class Target:
    _client = None

    def __init__(self):
        self._base_path = ""
        _build_resources(self, "_client", self._client)


def _build_resources(instance: type, attribute_name: str, value: type = None) -> None:
    """Add an attribute pointing to an instance for each resource.

    Args:
        instance (type): _description_
        attribute_name (str): _description_
        value (type, optional): _description_. Defaults to None.
    """
    if not value:
        value = instance

    for attribute in dir(instance):
        val = getattr(instance, attribute)

        try:
            if not issubclass(val, (SchemaBase, Target)):
                continue
        except TypeError:
            continue  # Failed because `issubclass` expects a class.

        setattr(val, attribute_name, value)


def clean_data(value: Any) -> Any:
    """Clean data for JSON serialization.

    Args:
        value (Any): The value to clean.

    Returns:
        Any: The cleaned value.
    """
    if isinstance(value, datetime):
        return clean_datetime(value)
    elif isinstance(value, date):
        return clean_date(value)
    elif isinstance(value, dict):
        return clean_request_payload(value)
    elif isinstance(value, list):
        return clean_json_list(value)
    elif isinstance(value, UUID):
        return str(value)

    # No cleaning needed
    return value


def clean_request_payload(payload: dict) -> dict:
    result = {}
    for k, v in payload.items():
        result[k] = clean_data(v)

    return result


def clean_json_list(data: list) -> list:
    result = []
    for item in data:
        result.append(clean_data(item))

    return result


def clean_request_params(params: dict) -> dict:
    result = {}
    for k, v in params.items():
        if isinstance(v, datetime):
            result[k] = clean_datetime(v)
        elif isinstance(v, date):
            result[k] = clean_date(v)
        elif isinstance(v, list):
            result[k] = ",".join(v)
        else:
            result[k] = v

    return result


def clean_date(date: date) -> str:
    dt = datetime(date.year, date.month, date.day, 0, 0, 0, tzinfo=timezone.utc)

    return clean_datetime(dt)


def clean_datetime(dt: datetime) -> str:
    return (
        dt.astimezone(tz=timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


def find_model_id(instance: Union[Collection, Resource], model_name: str) -> str:
    """Recursively traverse the `_parent` chain searching for a model id.

    Args:
        instance (Union[Collection, Resource]): The instanceect instance to inspect.
        model_name (str): The class name of the model to find.

    Raises:
        AttributeError: If recursion ends without finding the model id.

    Returns:
        str: The model id.
    """
    body_id_key = f"{to_camel_case(model_name)}Id"

    if instance.__class__.__name__ == model_name:
        return instance.id
    elif hasattr(instance, body_id_key):
        return getattr(instance, body_id_key)
    elif instance._parent is not None:
        return find_model_id(instance._parent, model_name)

    raise AttributeError(
        f"Cannot find {model_name} id. Model._parent chain ends in {instance}"
    )


def model_id(*models: Tuple[str]) -> Callable:
    """Insert values for `model_id` arguments if not provided.

    Args:
        *models (Tuple[str]): The model names to search for.

    Raises:
        TypeError: If no ID is found and no arguments are provided.
    """

    def decorator(f: Callable):
        @wraps(f)
        def wrapper(self, *args, **kwargs) -> Callable:
            outer_exc = None
            for model in models:
                key = f"{to_snake_case(model)}_id"

                if not args and key not in kwargs:
                    try:
                        kwargs[key] = find_model_id(self, model)
                    except AttributeError as e:
                        try:
                            raise e from outer_exc
                        except AttributeError as exc:
                            outer_exc = exc

            try:
                return f(self, *args, **kwargs)
            except TypeError as exc:
                # Raise from the outer `AttributeError` so we don't lose context.
                raise exc from outer_exc

        return wrapper

    return decorator


@lru_cache(maxsize=None)
def to_camel_case(s: str) -> str:
    """Convert a string to camelCase.

    Args:
        s (str): The string to convert.

    Returns:
        str: The converted camelCase string.
    """
    return inflection.camelize(to_snake_case(s), uppercase_first_letter=False)


@lru_cache(maxsize=None)
def to_snake_case(s: str) -> str:
    """Convert a string to snake_case.

    Args:
        s (str): The string to convert.

    Returns:
        str: The converted snake_case string.
    """
    return inflection.underscore(s)
