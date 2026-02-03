from datetime import datetime
from typing import Annotated

from fastapi import Depends, APIRouter
from pydantic import BeforeValidator

from models import (
    ResponseStatus,
    ResponseStatusListSchema,
    ResponseStatusList,
    SubscribeList,
    SubscribeListSchema,
)
import constants
from services import SubscribeService
from utils import parse_id_list

router = APIRouter()


@router.post(
    path=constants.SUBSCRIBES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.20.1 批量订阅消息",
)
async def create_subscrbe(
    data: SubscribeListSchema,
    service: Annotated[SubscribeService, Depends(SubscribeService)],
) -> ResponseStatusListSchema:
    subscribes = data.SubscribeListObject.SubscribeObject
    _ = await service.create_subscribes(subscribes=subscribes)

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.SUBSCRIBES_URL,
                    StatusCode="0",
                    StatusString="订阅成功",
                    Id=subscribe.SubscribeID,
                    LocalTime=datetime.now(),
                )
                for subscribe in subscribes
            ]
        )
    )


@router.get(
    path=constants.SUBSCRIBES_URL,
    response_model=SubscribeListSchema,
    description="GA/T 1400.4-2017 7.2.20.2 订阅任务的查询",
)
async def subscribes_query(
    service: Annotated[SubscribeService, Depends(SubscribeService)],
) -> SubscribeListSchema:
    """订阅任务的查询接口"""
    subscribes = await service.list_subscribes()
    return SubscribeListSchema(
        SubscribeListObject=SubscribeList(SubscribeObject=subscribes)
    )


@router.put(
    path=constants.SUBSCRIBES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.20.2 批量订阅的更新",
)
async def subscribes_update(
    data: SubscribeListSchema,
    service: Annotated[SubscribeService, Depends(SubscribeService)],
) -> ResponseStatusListSchema:
    """批量订阅修改接口"""
    subscribes = data.SubscribeListObject.SubscribeObject
    _ = await service.update_subscribes(subscribes)

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.SUBSCRIBES_URL,
                    StatusCode="0",
                    StatusString="修改成功",
                    Id=subscribe.SubscribeID,
                    LocalTime=datetime.now(),
                )
                for subscribe in subscribes
            ]
        )
    )


@router.delete(
    path=constants.SUBSCRIBES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.20.2 订阅任务的删除",
)
async def subscribes_delete(
    service: Annotated[SubscribeService, Depends(SubscribeService)],
    subscribe_ids: Annotated[list[str], BeforeValidator(parse_id_list)],
):
    """批量订阅删除接口"""
    _ = await service.delete_subscribe(subscribe_ids)

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.SUBSCRIBES_URL,
                    StatusCode="0",
                    StatusString="删除成功",
                    Id=subscribe_id,
                    LocalTime=datetime.now(),
                )
                for subscribe_id in subscribe_ids
            ]
        )
    )
