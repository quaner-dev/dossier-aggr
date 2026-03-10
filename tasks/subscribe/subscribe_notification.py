from core import brokers
from models import SubscribeNotification
from repo.subscribe.subscribe_notification import (
    create_subscribe_notifications_repo,
    delete_subscribe_notifications_repo,
    list_subscribe_notifications_repo,
)


async def list_subscribe_notifications_task(
    filters: dict[str, str] | None = None,
) -> list[SubscribeNotification]:
    """按过滤条件查询通知记录列表"""
    return list(await list_subscribe_notifications_repo(filters=filters))


@brokers.broker.task
async def create_subscribe_notifications_task(
    subscribe_notifications: list[SubscribeNotification],
):
    return await create_subscribe_notifications_repo(
        subscribe_notifications=subscribe_notifications
    )


@brokers.broker.task
async def delete_subscribe_notifications_task(notification_ids: list[str]) -> list[str]:
    return await delete_subscribe_notifications_repo(notification_ids=notification_ids)
