import asyncio
from types import SimpleNamespace

from api.subscribe.subscribe_notification import (
    subscribe_notifications_create,
    subscribe_notifications_delete,
    subscribe_notifications_query,
)
from models import (
    SubscribeNotification,
    ResponseStatusListSchema,
    SubscribeNotificationList,
    SubscribeNotificationListSchema,
)
from tests.type_helpers import as_service, as_status_list


class _FakeSubscribeNotificationService:
    def __init__(self):
        self.created_with: list[SubscribeNotification] | None = None
        self.deleted_with: list[str] | None = None
        self.query_filters: dict[str, str] | None = None
        self.notifications = _sample_notifications()

    async def create_subscribe_notifications(
        self, subscribe_notifications: list[SubscribeNotification]
    ):
        self.created_with = subscribe_notifications
        return subscribe_notifications

    async def list_subscribe_notifications(self, filters: dict[str, str] | None = None):
        self.query_filters = filters or {}
        notifications = self.notifications
        if "NotificationID" in self.query_filters:
            notifications = [
                n
                for n in notifications
                if n.NotificationID == self.query_filters["NotificationID"]
            ]
        return notifications

    async def delete_subscribe_notifications(self, notification_ids: list[str]):
        self.deleted_with = notification_ids
        return notification_ids


def _sample_notifications() -> list[SubscribeNotification]:
    return [
        SubscribeNotification(
            NotificationID="N-001",
            SubscribeID="S-001",
            Title="Notification-1",
            TriggerTime="20260101120000",
            InfoIDs="P-001,F-001",
            DeviceList=None,
            DataClassTabObjectList=None,
            ExecuteOperation=None,
            FaceObjectList=None,
            PersonObjectList=None,
        ),
        SubscribeNotification(
            NotificationID="N-002",
            SubscribeID="S-002",
            Title="Notification-2",
            TriggerTime="20260102120000",
            InfoIDs="P-002,F-002",
            DeviceList=None,
            DataClassTabObjectList=None,
            ExecuteOperation=None,
            FaceObjectList=None,
            PersonObjectList=None,
        ),
    ]


def test_subscribe_notifications_create_returns_status_list():
    async def _run():
        notifications = _sample_notifications()
        fake = _FakeSubscribeNotificationService()
        payload = SubscribeNotificationListSchema(
            SubscribeNotificationListObject=SubscribeNotificationList(
                SubscribeNotificationObject=notifications
            )
        )

        res = await subscribe_notifications_create(data=payload, service=as_service(fake))
        status = as_status_list(res.ResponseStatusListObject.ResponseStatusObject)

        assert len(status) == 2
        assert status[0].StatusCode == "0"
        assert status[0].Id == "N-001"
        assert fake.created_with is not None
        assert len(fake.created_with) == 2

    asyncio.run(_run())


def test_subscribe_notifications_query_returns_notification_list():
    async def _run():
        fake = _FakeSubscribeNotificationService()
        request = SimpleNamespace(query_params={"NotificationID": "N-001"})

        res = await subscribe_notifications_query(
            request=request,
            service=as_service(fake),
        )

        assert len(res.SubscribeNotificationListObject.SubscribeNotificationObject) == 1
        assert (
            res.SubscribeNotificationListObject.SubscribeNotificationObject[0].NotificationID
            == "N-001"
        )
        assert fake.query_filters == {"NotificationID": "N-001"}

    asyncio.run(_run())


def test_subscribe_notifications_delete_returns_status_list():
    async def _run():
        fake = _FakeSubscribeNotificationService()

        res = await subscribe_notifications_delete(
            service=as_service(fake),
            id_list=["N-001", "N-002"],
        )

        assert isinstance(res, ResponseStatusListSchema)
        status = as_status_list(res.ResponseStatusListObject.ResponseStatusObject)
        assert len(status) == 2
        assert status[0].Id == "N-001"
        assert status[1].Id == "N-002"
        assert fake.deleted_with == ["N-001", "N-002"]

    asyncio.run(_run())
