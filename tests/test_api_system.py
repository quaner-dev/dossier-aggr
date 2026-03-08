import asyncio
from datetime import datetime

from starlette.requests import Request

import constants
from api.system.keepalive import keepalive
from api.system.register import register
from api.system.time import system_time
from api.system.unregister import unregister
from models import KeepaliveSchema, RegisterSchema, SystemTime, UnRegisterSchema
from tests.type_helpers import as_service, as_status_list, dt


class _FakeAPSService:
    def __init__(self):
        self.updated_ids: list[str] = []

    async def update_aps(self, aps_id: str):
        self.updated_ids.append(aps_id)
        return aps_id


class _FakeSystemTimeService:
    async def get_system_time(self):
        return SystemTime(LocalTime=dt("20260302091530"))


def _make_request(path: str) -> Request:
    scope = {
        "type": "http",
        "method": "POST",
        "path": path,
        "headers": [],
        "scheme": "http",
        "server": ("testserver", 80),
        "client": ("testclient", 50000),
        "root_path": "",
        "query_string": b"",
    }
    return Request(scope)


def test_register_returns_success_status():
    async def _run():
        fake = _FakeAPSService()
        payload = RegisterSchema.model_validate(
            {"RegisterObject": {"DeviceID": "APS-001"}}
        )

        res = await register(
            request=_make_request(constants.REGISTER_URL),
            data=payload,
            service=as_service(fake),
        )

        status = as_status_list(res.ResponseStatusObject)
        assert status[0].StatusCode == "0"
        assert constants.REGISTER_URL in status[0].RequestURL
        assert fake.updated_ids == ["APS-001"]

    asyncio.run(_run())


def test_unregister_returns_success_status():
    async def _run():
        fake = _FakeAPSService()
        payload = UnRegisterSchema.model_validate(
            {"UnRegisterObject": {"DeviceID": "APS-002"}}
        )

        res = await unregister(data=payload, service=as_service(fake))

        assert res.StatusCode == "0"
        assert res.RequestURL == constants.UNREGISTER_URL
        assert fake.updated_ids == ["APS-002"]

    asyncio.run(_run())


def test_keepalive_returns_success_status():
    async def _run():
        fake = _FakeAPSService()
        payload = KeepaliveSchema.model_validate(
            {"KeepaliveObject": {"DeviceID": "APS-003"}}
        )

        res = await keepalive(data=payload, service=as_service(fake))

        assert res.StatusCode == "0"
        assert res.RequestURL == constants.KEEPALIVE_URL
        assert fake.updated_ids == ["APS-003"]

    asyncio.run(_run())


def test_system_time_returns_current_time_schema():
    async def _run():
        fake = _FakeSystemTimeService()
        res = await system_time(service=as_service(fake))

        assert res.LocalTime == datetime.strptime("20260302091530", "%Y%m%d%H%M%S")

    asyncio.run(_run())
