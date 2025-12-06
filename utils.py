from datetime import datetime


def parse_datetime(v: str | datetime) -> datetime:
    if isinstance(v, str):
        return datetime.strptime(v, "%Y%m%d%H%M%S")
    return v


def serialize_datetime(v: str | datetime) -> str:
    if isinstance(v, datetime):
        return datetime.strftime(v, "%Y%m%d%H%M%S")
    return v
