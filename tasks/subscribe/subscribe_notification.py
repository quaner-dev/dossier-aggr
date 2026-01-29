import brokers
from models import SubscribeNotification


@brokers.broker.task
async def create_subscribe_notification(
    subscribe_notification: SubscribeNotification,
): ...
