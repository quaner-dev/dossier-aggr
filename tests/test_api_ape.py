import asyncio

from api.collection.ape import apes_query, apes_update
from domain import APE
from domain.common import enums
from schemas import APEList, APEListSchema
from tests.type_helpers import as_service, as_status_list


class _FakeAPEService:
    def __init__(self, apes: list[APE]):
        self._apes = apes
        self.update_called_with: list[APE] | None = None

    async def list_apes(self):
        return self._apes

    async def update_apes(self, apes: list[APE]):
        self.update_called_with = apes
        return apes


def _sample_apes() -> list[APE]:
    return [
        APE(
            ApeID="APE-001",
            Name="Camera-1",
            Model="Model-X",
            IPAddr="192.168.1.10",
            IPV6Addr=None,
            Port=8080,
            Longitude=116.3913,
            Latitude=39.9075,
            PlaceCode="110000",
            Place="Beijing",
            OrgCode="110101",
            CapDirection=enums.CapDirectionEnum.Front,
            MonitorDirection=enums.MonitorDirectionEnum.WestToEast,
            MonitorAreaDesc="Gate",
            IsOnline=enums.StatusTypeEnum.Online,
            OwnerApsID="APS-001",
            UserId="admin",
            Password="pass",
            FunctionType="Capture",
            PositionType="Fixed",
        ),
        APE(
            ApeID="APE-002",
            Name="Camera-2",
            Model="Model-Y",
            IPAddr="192.168.1.11",
            IPV6Addr=None,
            Port=8081,
            Longitude=121.4737,
            Latitude=31.2304,
            PlaceCode="310000",
            Place="Shanghai",
            OrgCode="310101",
            CapDirection=enums.CapDirectionEnum.Rear,
            MonitorDirection=enums.MonitorDirectionEnum.EastToWest,
            MonitorAreaDesc="Road",
            IsOnline=enums.StatusTypeEnum.Offline,
            OwnerApsID="APS-002",
            UserId="admin",
            Password="pass",
            FunctionType="Capture",
            PositionType="Fixed",
        ),
    ]


def test_apes_query_returns_list():
    async def _run():
        apes = _sample_apes()
        fake = _FakeAPEService(apes)
        res = await apes_query(service=as_service(fake))

        assert res.APEListObject.APEObject[0].ApeID == "APE-001"
        assert len(res.APEListObject.APEObject) == 2

    asyncio.run(_run())


def test_apes_update_returns_status_list():
    async def _run():
        apes = _sample_apes()
        fake = _FakeAPEService(apes)
        payload = APEListSchema(APEListObject=APEList(APEObject=apes))

        res = await apes_update(data=payload, service=as_service(fake))

        status_obj = as_status_list(res.ResponseStatusListObject.ResponseStatusObject)
        assert len(status_obj) == 2
        assert status_obj[0].StatusCode == "0"
        assert status_obj[0].Id == "APE-001"
        assert fake.update_called_with is not None
        assert len(fake.update_called_with) == 2

    asyncio.run(_run())
