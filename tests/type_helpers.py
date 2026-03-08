from datetime import datetime
from typing import Any

from models import ResponseStatus


def as_service(service: object) -> Any:
    return service


def as_status_list(
    value: ResponseStatus | list[ResponseStatus],
) -> list[ResponseStatus]:
    if isinstance(value, list):
        return value
    return [value]


def dt(value: str) -> datetime:
    return datetime.strptime(value, "%Y%m%d%H%M%S")
