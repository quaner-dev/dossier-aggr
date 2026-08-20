from datetime import UTC, datetime

from core.time import CHINA_TZ
from core.utils import parse_datetime, serialize_datetime


def test_parse_datetime_interprets_protocol_value_as_china_time():
    value = parse_datetime("20260302091530")

    assert value == datetime(2026, 3, 2, 9, 15, 30, tzinfo=CHINA_TZ)


def test_parse_datetime_interprets_naive_value_as_china_time():
    value = parse_datetime(datetime.fromisoformat("2026-03-02T09:15:30"))

    assert value == datetime(2026, 3, 2, 9, 15, 30, tzinfo=CHINA_TZ)


def test_serialize_datetime_converts_aware_value_to_china_time():
    value = datetime(2026, 3, 2, 1, 15, 30, tzinfo=UTC)

    assert serialize_datetime(value) == "20260302091530"


def test_serialize_datetime_interprets_naive_value_as_china_time():
    value = datetime.fromisoformat("2026-03-02T09:15:30")

    assert serialize_datetime(value) == "20260302091530"
