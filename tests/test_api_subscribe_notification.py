import asyncio

from api.subscribe.subscribe_notification import (
    subscribe_notification_get,
    subscribe_notifications_create,
)
from models import (
    SubscribeNotification,
    SubscribeNotificationList,
    SubscribeNotificationListSchema,
)
from tests.type_helpers import as_service, as_status_list


class _FakeSubscribeNotificationService:
    def __init__(self):
        self.created_with: list[SubscribeNotification] | None = None
        self.notifications = _sample_notifications()

    async def create_subscribe_notifications(
        self, subscribe_notifications: list[SubscribeNotification]
    ):
        self.created_with = subscribe_notifications
        return subscribe_notifications

    async def get_subscribe_notification(self, notification_id: str):
        return next(
            n for n in self.notifications if n.NotificationID == notification_id
        )


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


def test_subscribe_notification_get_returns_single_notification():
    async def _run():
        fake = _FakeSubscribeNotificationService()

        res = await subscribe_notification_get(
            notification_id="N-001",
            service=as_service(fake),
        )

        assert res.NotificationID == "N-001"
        assert res.SubscribeID == "S-001"

    asyncio.run(_run())
