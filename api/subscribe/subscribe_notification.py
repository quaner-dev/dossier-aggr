from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from models import (
    ResponseStatusListSchema,
    SubscribeNotificationListSchema,
    ResponseStatus,
    ResponseStatusList,
)
import constants
from services import SubscribeNotificationService

router = APIRouter()


@router.post(
    path=constants.SUBSCRIBE_NOTIFICATIONS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.21.1 通知消息",
)
async def subscribe_notifications_create(
    data: SubscribeNotificationListSchema,
    service: Annotated[
        SubscribeNotificationService, Depends(SubscribeNotificationService)
    ],
):
    subscribe_notifications = (
        data.SubscribeNotificationListObject.SubscribeNotificationObject
    )
    await service.batch_create_subscribe_notifications(subscribe_notifications)

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.SUBSCRIBE_NOTIFICATIONS_URL,
            StatusCode="0",
            StatusString="通知成功",
            Id=subscribe_notification.NotificationID,
            LocalTime=datetime.now(),
        )
        for subscribe_notification in subscribe_notifications
    ]
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )
