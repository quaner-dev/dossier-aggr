from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from models import (
    ResponseStatusListSchema,
    SubscribeNotification,
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
    _ = await service.create_subscribe_notifications(subscribe_notifications)

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.SUBSCRIBE_NOTIFICATIONS_URL,
                    StatusCode="0",
                    StatusString="通知成功",
                    Id=subscribe_notification.NotificationID,
                    LocalTime=datetime.now(),
                )
                for subscribe_notification in subscribe_notifications
            ]
        )
    )


@router.get(
    path=f"{constants.SUBSCRIBE_NOTIFICATIONS_URL}/{{notification_id}}",
    response_model=SubscribeNotification,
    description="GA/T 1400.4-2017 7.2.21.2 单条通知记录查询",
)
async def subscribe_notification_get(
    notification_id: str,
    service: Annotated[
        SubscribeNotificationService, Depends(SubscribeNotificationService)
    ],
) -> SubscribeNotification:
    """单条通知记录查询接口"""
    return await service.get_subscribe_notification(notification_id=notification_id)
