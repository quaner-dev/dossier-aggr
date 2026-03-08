from models import SubscribeNotification
from repositories.subscribe.subscribe_notification import (
    get_subscribe_notification_repo,
)
from tasks import create_subscribe_notifications_task
from services.task_dispatch import dispatch_and_wait


class SubscribeNotificationService:
    async def get_subscribe_notification(
        self,
        notification_id: str,
    ) -> SubscribeNotification:
        return await get_subscribe_notification_repo(notification_id=notification_id)

    async def create_subscribe_notifications(
        self, subscribe_notifications: list[SubscribeNotification]
    ):
        return await dispatch_and_wait(
            create_subscribe_notifications_task,
            subscribe_notifications=subscribe_notifications
        )
