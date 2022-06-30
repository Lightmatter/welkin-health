from datetime import datetime, timezone


def clean_request_payload(payload: dict) -> dict:
    for k, v in payload.items():
        if isinstance(v, datetime):
            payload[k] = clean_datetime(v)

    return payload


def clean_datetime(dt: datetime) -> str:
    return (
        dt.astimezone(tz=timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )
