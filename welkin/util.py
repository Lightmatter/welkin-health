from datetime import datetime, timezone

# NOTE: `clean_request_payload` and `clean_request_params` are intentionally DRY
# violations. The code may be the same, but they represent different knowledge.


def clean_request_payload(payload: dict) -> dict:
    for k, v in payload.items():
        if isinstance(v, datetime):
            payload[k] = clean_datetime(v)

    return payload


def clean_request_params(params: dict) -> dict:
    for k, v in params.items():
        if isinstance(v, datetime):
            params[k] = clean_datetime(v)

    return params


def clean_datetime(dt: datetime) -> str:
    return (
        dt.astimezone(tz=timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )
