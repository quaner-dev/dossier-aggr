from models import SubscribeNotification
from tasks import create_subscribe_notification


class SubscribeNotificationService:
    async def create_subscribe_notification(
        self, subscribe_notification: SubscribeNotification
    ):
        await create_subscribe_notification.kiq(subscribe_notification)

    async def batch_create_subscribe_notifications(
        self, subscribe_notifications: list[SubscribeNotification]
    ):
        for subscribe_notification in subscribe_notifications:
            await create_subscribe_notification.kiq(subscribe_notification)
