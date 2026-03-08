import asyncio

from api.subscribe.subscrbe import (
    create_subscrbe,
    subscribe_cancel,
    subscribes_query,
    subscribes_update,
    subscribes_delete,
)
from models import Subscribe, SubscribeList, SubscribeListSchema
from models.common import enums
from tests.type_helpers import as_service, as_status_list


class _FakeSubscribeService:
    def __init__(self, subscribes: list[Subscribe]):
        self._subscribes = subscribes
        self.created_with: list[Subscribe] | None = None
        self.updated_with: list[Subscribe] | None = None
        self.deleted_with: list[str] | None = None

    async def create_subscribes(self, subscribes: list[Subscribe]):
        self.created_with = subscribes
        return subscribes

    async def list_subscribes(self):
        return self._subscribes

    async def update_subscribes(self, subscribes: list[Subscribe]):
        self.updated_with = subscribes
        return subscribes

    async def delete_subscribe(self, subscribe_ids: list[str]):
        self.deleted_with = subscribe_ids
        return subscribe_ids

    async def update_subscribe_by_id(self, subscribe_id: str, subscribe: Subscribe):
        subscribe.SubscribeID = subscribe_id
        return subscribe


def _sample_subscribes() -> list[Subscribe]:
    return [
        Subscribe(
            SubscribeID="S-001",
            Title="Subscribe-1",
            SubscribeDetail="face",
            ResourceClass=enums.ResourceClassEnum.Ape,
            ResourceURI="/VIID/Faces",
            ApplicantName="tester",
            ApplicantOrg="org",
            BeginTime="20260101120000",
            EndTime="20270101120000",
            ReceiveAddr="http://127.0.0.1/callback",
            ReportInterval=30,
            Reason="test",
            OperateType=enums.OperateTypeEnum.Subscribe,
            SubscribeStatus=enums.SubscribeStatusEnum.Active,
            SubscribeCancelOrg=None,
            SubscribeCancelPerson=None,
            CancelTime=None,
            CancelReason=None,
            ResultImageDeclare=enums.ResultImageDeclareEnum.FaceImage,
            ResultFeatureDeclare=enums.ResultFeatureDeclareEnum.WithFeatures,
            TabID=None,
        ),
        Subscribe(
            SubscribeID="S-002",
            Title="Subscribe-2",
            SubscribeDetail="person",
            ResourceClass=enums.ResourceClassEnum.Ape,
            ResourceURI="/VIID/Persons",
            ApplicantName="tester",
            ApplicantOrg="org",
            BeginTime="20260102120000",
            EndTime="20270102120000",
            ReceiveAddr="http://127.0.0.1/callback",
            ReportInterval=60,
            Reason=None,
            OperateType=enums.OperateTypeEnum.Subscribe,
            SubscribeStatus=enums.SubscribeStatusEnum.Active,
            SubscribeCancelOrg=None,
            SubscribeCancelPerson=None,
            CancelTime=None,
            CancelReason=None,
            ResultImageDeclare=enums.ResultImageDeclareEnum.PersonImage,
            ResultFeatureDeclare=enums.ResultFeatureDeclareEnum.WithoutFeatures,
            TabID=None,
        ),
    ]


def test_subscribes_query_returns_list():
    async def _run():
        subscribes = _sample_subscribes()
        fake = _FakeSubscribeService(subscribes)

        res = await subscribes_query(service=as_service(fake))

        assert len(res.SubscribeListObject.SubscribeObject) == 2
        assert res.SubscribeListObject.SubscribeObject[0].SubscribeID == "S-001"

    asyncio.run(_run())


def test_subscribes_create_update_delete_return_status_list():
    async def _run():
        subscribes = _sample_subscribes()
        fake = _FakeSubscribeService(subscribes)
        payload = SubscribeListSchema(
            SubscribeListObject=SubscribeList(SubscribeObject=subscribes)
        )

        create_res = await create_subscrbe(data=payload, service=as_service(fake))
        update_res = await subscribes_update(data=payload, service=as_service(fake))
        delete_res = await subscribes_delete(
            service=as_service(fake), subscribe_ids=["S-001", "S-002"]
        )

        create_status = as_status_list(
            create_res.ResponseStatusListObject.ResponseStatusObject
        )
        update_status = as_status_list(
            update_res.ResponseStatusListObject.ResponseStatusObject
        )
        delete_status = as_status_list(
            delete_res.ResponseStatusListObject.ResponseStatusObject
        )

        assert len(create_status) == 2
        assert create_status[0].StatusCode == "0"
        assert create_status[0].Id == "S-001"
        assert len(update_status) == 2
        assert update_status[1].Id == "S-002"
        assert len(delete_status) == 2
        assert delete_status[0].Id == "S-001"

        assert fake.created_with is not None
        assert len(fake.created_with) == 2
        assert fake.updated_with is not None
        assert len(fake.updated_with) == 2
        assert fake.deleted_with == ["S-001", "S-002"]

    asyncio.run(_run())


def test_subscribe_cancel_by_id_returns_status():
    async def _run():
        subscribes = _sample_subscribes()
        fake = _FakeSubscribeService(subscribes)
        payload = subscribes[0]

        res = await subscribe_cancel(
            subscribe_id="S-001",
            data=payload,
            service=as_service(fake),
        )

        assert res.StatusCode == "0"
        assert res.Id == "S-001"
        assert res.RequestURL.endswith("/VIID/Subscribes/S-001")

    asyncio.run(_run())
