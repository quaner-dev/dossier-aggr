from datetime import datetime

from fastapi import APIRouter

import tasks
import schemas
import constants

router = APIRouter()


@router.post(
    path=constants.SUBSCRIBE_NOTIFICATIONS_URL,
    response_model=schemas.ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.21.1 通知消息",
)
async def subscribe_notifications_create(
    data: schemas.subscribe_notification.SubscribeNotificationListSchema,
):
    subscribe_notifications = (
        data.SubscribeNotificationListObject.SubscribeNotificationObject
    )
    for subscribe_notification in subscribe_notifications:
        await tasks.create_subscribe_notification.kiq(subscribe_notification)

    response_status_objects = [
        schemas.ResponseStatus(
            RequestURL=constants.SUBSCRIBE_NOTIFICATIONS_URL,
            StatusCode="0",
            StatusString="通知成功",
            Id=subscribe_notification.NotificationID,
            LocalTime=datetime.now(),
        )
        for subscribe_notification in subscribe_notifications
    ]
    return schemas.ResponseStatusListSchema(
        ResponseStatusListObject=schemas.ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )
