import asyncio

from api.collection.aps import list_aps
from models import APS
from models.common import enums
from tests.type_helpers import as_service


class _FakeAPSService:
    def __init__(self, apss: list[APS]):
        self._apss = apss

    async def list_apss(self):
        return self._apss


def _sample_apss() -> list[APS]:
    return [
        APS(
            ApsID="APS-001",
            Name="Collect-1",
            IPAddr="192.168.1.1",
            IPV6Addr=None,
            Port=8000,
            IsOnline=enums.StatusTypeEnum.Online,
        ),
        APS(
            ApsID="APS-002",
            Name="Collect-2",
            IPAddr="192.168.1.2",
            IPV6Addr=None,
            Port=8001,
            IsOnline=enums.StatusTypeEnum.Offline,
        ),
    ]


def test_list_aps_returns_list():
    async def _run():
        apss = _sample_apss()
        fake = _FakeAPSService(apss)

        res = await list_aps(service=as_service(fake))

        assert len(res.APSListObject.APSObject) == 2
        assert res.APSListObject.APSObject[0].ApsID == "APS-001"

    asyncio.run(_run())
