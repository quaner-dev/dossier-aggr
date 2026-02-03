import brokers
from models import SubscribeNotification
from sqlmodel.ext.asyncio.session import AsyncSession
from database import engine


@brokers.broker.task
async def create_subscribe_notifications_task(
    subscribe_notifications: list[SubscribeNotification],
):
    async with AsyncSession(engine) as session:
        session.add_all(subscribe_notifications)
        await session.commit()
        await session.refresh(subscribe_notifications)
    return subscribe_notifications
