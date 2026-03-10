from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from pydantic import BeforeValidator

from models import (
    ResponseStatusListSchema,
    SubscribeNotificationList,
    SubscribeNotificationListSchema,
    ResponseStatus,
    ResponseStatusList,
)
from core import constants
from services import SubscribeNotificationService
from core.utils import parse_id_list

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
    path=constants.SUBSCRIBE_NOTIFICATIONS_URL,
    response_model=SubscribeNotificationListSchema,
    description="GA/T 1400.4-2017 7.2.21.2 通知记录查询",
)
async def subscribe_notifications_query(
    request: Request,
    service: Annotated[
        SubscribeNotificationService, Depends(SubscribeNotificationService)
    ],
) -> SubscribeNotificationListSchema:
    """批量通知记录查询接口"""
    filters = dict(request.query_params)
    notifications = await service.list_subscribe_notifications(filters=filters)
    return SubscribeNotificationListSchema(
        SubscribeNotificationListObject=SubscribeNotificationList(
            SubscribeNotificationObject=notifications
        )
    )


@router.delete(
    path=constants.SUBSCRIBE_NOTIFICATIONS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.21.2 通知记录删除",
)
async def subscribe_notifications_delete(
    service: Annotated[
        SubscribeNotificationService, Depends(SubscribeNotificationService)
    ],
    id_list: Annotated[list[str], BeforeValidator(parse_id_list), Query(alias="IDList")],
) -> ResponseStatusListSchema:
    notification_ids = await service.delete_subscribe_notifications(
        notification_ids=id_list
    )
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.SUBSCRIBE_NOTIFICATIONS_URL,
                    StatusCode="0",
                    StatusString="删除成功",
                    Id=notification_id,
                    LocalTime=datetime.now(),
                )
                for notification_id in notification_ids
            ]
        )
    )
