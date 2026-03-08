import exceptions
from database import engine
from models import SubscribeNotification
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


async def get_subscribe_notification_repo(
    notification_id: str,
) -> SubscribeNotification:
    """根据通知ID查询单条订阅通知"""
    async with AsyncSession(engine) as session:
        statement = select(SubscribeNotification).where(
            SubscribeNotification.NotificationID == notification_id
        )
        notification = (await session.exec(statement)).first()
        if not notification:
            raise exceptions.DataNotFoundError(detail=f"{notification_id} not found")
        return notification


async def create_subscribe_notifications_repo(
    subscribe_notifications: list[SubscribeNotification],
) -> list[SubscribeNotification]:
    """创建通知记录"""
    async with AsyncSession(engine) as session:
        session.add_all(subscribe_notifications)
        await session.commit()
        for notification in subscribe_notifications:
            await session.refresh(notification)
    return subscribe_notifications
