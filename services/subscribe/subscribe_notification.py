from models import SubscribeNotification
from repo.subscribe.subscribe_notification import (
    create_subscribe_notifications_repo,
    delete_subscribe_notifications_repo,
    list_subscribe_notifications_repo,
)


class SubscribeNotificationService:
    """编排 GA/T 1400 订阅通知业务链路。

    通知查询、创建和删除统一委托 repo。
    """

    async def list_subscribe_notifications(
        self, filters: dict[str, str] | None = None
    ) -> list[SubscribeNotification]:
        return list(await list_subscribe_notifications_repo(filters=filters))

    async def create_subscribe_notifications(
        self, subscribe_notifications: list[SubscribeNotification]
    ) -> list[SubscribeNotification]:
        return list(
            await create_subscribe_notifications_repo(
                subscribe_notifications=subscribe_notifications
            )
        )

    async def delete_subscribe_notifications(
        self, notification_ids: list[str]
    ) -> list[str]:
        return await delete_subscribe_notifications_repo(
            notification_ids=notification_ids
        )
