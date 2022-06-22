from datetime import datetime, timezone


def clean_datetime(dt: datetime):
    return (
        dt.astimezone(tz=timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )
