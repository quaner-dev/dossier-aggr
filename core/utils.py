from datetime import datetime


def parse_datetime(v: str | datetime) -> datetime:
    if isinstance(v, str):
        return datetime.strptime(v, "%Y%m%d%H%M%S")
    return v


def serialize_datetime(v: str | datetime) -> str:
    if isinstance(v, datetime):
        return datetime.strftime(v, "%Y%m%d%H%M%S")
    return v


def parse_id_list(v: str | list[str]) -> list[str]:
    raw_values = v if isinstance(v, list) else [str(v)]
    parsed_values: list[str] = []
    for raw_value in raw_values:
        parsed_values.extend(
            item.strip() for item in str(raw_value).split(",") if item.strip()
        )
    return parsed_values
