from datetime import datetime

from fastapi import Depends, APIRouter, Query

from schemas import (
    ResponseStatus,
    ResponseStatusListSchema,
    ResponseStatusList,
    SubscribeListSchema,
)
import constants
from services import SubscribeService

router = APIRouter()


@router.get(
    path=constants.SUBSCRIBES_URL,
    response_model=SubscribeListSchema,
    description="GA/T 1400.4-2017 7.2.20.4 订阅查询",
)
async def subscribes_query(
    subscribe_id: str | None = Query(None, alias="SubscribeID", max_length=33),
    service: SubscribeService = Depends(SubscribeService),
):
    """订阅查询接口"""
    from schemas.subscribe import SubscribeList
    
    if subscribe_id:
        subscribe = await service.get_subscribe(subscribe_id)
        return SubscribeListSchema(SubscribeListObject=SubscribeList(SubscribeObject=[subscribe]))
    else:
        subscribes = await service.list_subscribes()
        return SubscribeListSchema(SubscribeListObject=SubscribeList(SubscribeObject=subscribes))


@router.post(
    path=constants.SUBSCRIBES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.20.1 批量订阅消息",
)
async def create_subscrbe(
    data: SubscribeListSchema,
    service: SubscribeService = Depends(SubscribeService),
):
    subscribes = data.SubscribeListObject.SubscribeObject
    await service.batch_create_subscribe(subscribes)

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.SUBSCRIBES_URL,
            StatusCode="0",
            StatusString="订阅成功",
            Id=subscribe.SubscribeID,
            LocalTime=datetime.now(),
        )
        for subscribe in subscribes
    ]

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )


@router.put(
    path=constants.SUBSCRIBES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.20.2 批量订阅修改",
)
async def subscribes_update(
    data: SubscribeListSchema,
    service: SubscribeService = Depends(SubscribeService),
):
    """批量订阅修改接口"""
    subscribes = data.SubscribeListObject.SubscribeObject
    for subscribe in subscribes:
        await service.update_subscribe(subscribe.SubscribeID, subscribe)

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.SUBSCRIBES_URL,
            StatusCode="0",
            StatusString="修改成功",
            Id=subscribe.SubscribeID,
            LocalTime=datetime.now(),
        )
        for subscribe in subscribes
    ]

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )


@router.delete(
    path=constants.SUBSCRIBES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.20.3 批量订阅删除",
)
async def subscribes_delete(
    id_list: str = Query(..., alias="IDList"),
    service: SubscribeService = Depends(SubscribeService),
):
    """批量订阅删除接口"""
    subscribe_ids = [id.strip() for id in id_list.split(",")]
    
    for subscribe_id in subscribe_ids:
        await service.delete_subscribe(subscribe_id)

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.SUBSCRIBES_URL,
            StatusCode="0",
            StatusString="删除成功",
            Id=subscribe_id,
            LocalTime=datetime.now(),
        )
        for subscribe_id in subscribe_ids
    ]

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )
