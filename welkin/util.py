import functools
import re
from datetime import date, datetime, timezone
from typing import Any
from uuid import UUID

from welkin.models.base import SchemaBase

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


def find_model_id(obj, model: str):
    if obj.__class__.__name__ == model:
        return obj.id
    elif hasattr(obj, f"{to_snake_case(model)}Id"):
        return obj.patientId
    elif obj._parent:
        return find_model_id(obj._parent, model)

    raise AttributeError(f"Cannot find {model} id. Model._parent chain ends in {obj}")


def model_id(*models):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            outer_exc = None
            for model in models:
                key = f"{to_snake_case(model)}_id"

                if not args and key not in kwargs:
                    try:
                        kwargs[key] = find_model_id(self, model)
                    except AttributeError as exc:
                        outer_exc = exc

            try:
                return f(self, *args, **kwargs)
            except TypeError as exc:
                raise exc from outer_exc

        return wrapper

    return decorator


def to_snake_case(s):
    first = re.compile(r"(.)([A-Z][a-z]+)")
    second = re.compile(r"([a-z0-9])([A-Z])")
    repl = r"\1_\2"

    return second.sub(repl, first.sub(repl, s)).lower()
