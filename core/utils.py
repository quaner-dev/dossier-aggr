from datetime import datetime

from core.time import CHINA_TZ


def parse_datetime(v: str | datetime) -> datetime:
    if isinstance(v, str):
        return datetime.strptime(v, "%Y%m%d%H%M%S").replace(tzinfo=CHINA_TZ)
    if v.tzinfo is None:
        return v.replace(tzinfo=CHINA_TZ)
    return v


def serialize_datetime(v: str | datetime) -> str:
    if isinstance(v, datetime):
        if v.tzinfo is None:
            v = v.replace(tzinfo=CHINA_TZ)
        else:
            v = v.astimezone(CHINA_TZ)
        return v.strftime("%Y%m%d%H%M%S")
    return v


def parse_id_list(v: str | list[str]) -> list[str]:
    raw_values = v if isinstance(v, list) else [str(v)]
    parsed_values: list[str] = []
    for raw_value in raw_values:
        parsed_values.extend(
            item.strip() for item in str(raw_value).split(",") if item.strip()
        )
    return parsed_values
