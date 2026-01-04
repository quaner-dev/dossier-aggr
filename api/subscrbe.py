from datetime import datetime

from fastapi import Depends, APIRouter

import schemas
import services
import constants

router = APIRouter()


@router.post(
    path=constants.SUBSCRIBES_URL,
    response_model=schemas.ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.20.1 批量订阅消息",
)
async def subscrbe(
    data: schemas.subscribe.SubscribeListSchema,
    service: services.subscribe.SubscribeService = Depends(
        services.subscribe.SubscribeService
    ),
):
    subscribes = data.SubscribeListObject.SubscribeObject
    await service.batch_create(subscribes)

    response_status_objects = [
        schemas.ResponseStatus(
            RequestURL=constants.SUBSCRIBES_URL,
            StatusCode="0",
            StatusString="订阅成功",
            Id=subscribe.SubscribeID,
            LocalTime=datetime.now(),
        )
        for subscribe in subscribes
    ]

    return schemas.ResponseStatusListSchema(
        ResponseStatusListObject=schemas.ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )
