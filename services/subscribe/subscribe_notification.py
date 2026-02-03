from models import SubscribeNotification
from tasks import create_subscribe_notifications_task


class SubscribeNotificationService:
    async def create_subscribe_notifications(
        self, subscribe_notifications: list[SubscribeNotification]
    ):
        return await create_subscribe_notifications_task.kiq(
            subscribe_notifications=subscribe_notifications
        )
