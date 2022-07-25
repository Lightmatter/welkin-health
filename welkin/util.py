from datetime import datetime, timezone

# NOTE: `clean_request_payload` and `clean_request_params` are intentionally DRY
# violations. The code may be the same, but they represent different knowledge.
# the same goes for `clean_request_payload` and `clean_json_list`


def clean_request_payload(payload: dict) -> dict:
    for k, v in payload.items():
        if isinstance(v, datetime):
            payload[k] = clean_datetime(v)
        elif isinstance(v, dict):
            payload[k] = clean_request_payload(v)
        elif isinstance(v, list):
            payload[k] = clean_json_list(v)

    return payload


def clean_json_list(data: list) -> list:
    for ind, item in enumerate(data):
        if isinstance(item, datetime):
            data[ind] = clean_datetime(item)
        elif isinstance(item, dict):
            data[ind] = clean_request_payload(item)
        elif isinstance(item, list):
            data[ind] = clean_json_list(item)

    return data


def clean_request_params(params: dict) -> dict:
    for k, v in params.items():
        if isinstance(v, datetime):
            params[k] = clean_datetime(v)
        elif isinstance(v, list):
            params[k] = ",".join(v)

    return params


def clean_datetime(dt: datetime) -> str:
    return (
        dt.astimezone(tz=timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )
