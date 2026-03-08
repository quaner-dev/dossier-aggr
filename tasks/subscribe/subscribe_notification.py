import brokers
from models import SubscribeNotification
from repositories.subscribe.subscribe_notification import (
    create_subscribe_notifications_repo,
    get_subscribe_notification_repo,
)


async def get_subscribe_notification_task(notification_id: str) -> SubscribeNotification:
    """根据通知ID查询单条订阅通知"""
    return await get_subscribe_notification_repo(notification_id=notification_id)


@brokers.broker.task
async def create_subscribe_notifications_task(
    subscribe_notifications: list[SubscribeNotification],
):
    return await create_subscribe_notifications_repo(
        subscribe_notifications=subscribe_notifications
    )
