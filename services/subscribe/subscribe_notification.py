from models import SubscribeNotification
from repositories.subscribe.subscribe_notification import (
    list_subscribe_notifications_repo,
)
from tasks import (
    create_subscribe_notifications_task,
    delete_subscribe_notifications_task,
)
from services.task_dispatch import dispatch_and_wait


class SubscribeNotificationService:
    async def list_subscribe_notifications(
        self, filters: dict[str, str] | None = None
    ) -> list[SubscribeNotification]:
        return list(await list_subscribe_notifications_repo(filters=filters))

    async def create_subscribe_notifications(
        self, subscribe_notifications: list[SubscribeNotification]
    ):
        return await dispatch_and_wait(
            create_subscribe_notifications_task,
            subscribe_notifications=subscribe_notifications,
        )

    async def delete_subscribe_notifications(
        self, notification_ids: list[str]
    ) -> list[str]:
        return await dispatch_and_wait(
            delete_subscribe_notifications_task,
            notification_ids=notification_ids,
        )
