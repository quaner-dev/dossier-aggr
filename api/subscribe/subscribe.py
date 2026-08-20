from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from core import constants, exceptions
from core.time import CHINA_TZ
from core.utils import parse_id_list
from models import (
    ResponseStatus,
    ResponseStatusList,
    ResponseStatusListSchema,
    Subscribe,
    SubscribeList,
    SubscribeListSchema,
)
from services import SubscribeService

router = APIRouter()


@router.post(
    path=constants.SUBSCRIBES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.20.1 批量订阅消息",
)
async def subscribes_create(
    data: SubscribeListSchema,
    service: Annotated[SubscribeService, Depends(SubscribeService)],
) -> ResponseStatusListSchema:
    """处理 7.2.20.1 批量订阅消息并返回逐订阅状态。"""

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
                    LocalTime=datetime.now(tz=CHINA_TZ),
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
    """处理 7.2.20.2 订阅任务查询并包装 `SubscribeListObject`。"""

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
    """处理 7.2.20.2 批量订阅更新并返回逐订阅状态。"""

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
                    LocalTime=datetime.now(tz=CHINA_TZ),
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
    subscribe_ids: Annotated[
        str | list[str] | None,
        Query(alias="IDList"),
    ] = None,
    legacy_subscribe_ids: Annotated[
        str | list[str] | None,
        Query(alias="subscribe_ids", include_in_schema=False),
    ] = None,
):
    """处理 7.2.20.2 订阅任务批量删除。

    正式参数为 `IDList`；`subscribe_ids` 仅作为旧调用兼容入口，
    不进入 OpenAPI 协议说明。
    """

    raw_subscribe_ids = (
        subscribe_ids if subscribe_ids is not None else legacy_subscribe_ids
    )
    if raw_subscribe_ids is None:
        raise exceptions.InvalidParameterError(detail="IDList is required")

    parsed_subscribe_ids = parse_id_list(raw_subscribe_ids)
    _ = await service.delete_subscribe(parsed_subscribe_ids)

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.SUBSCRIBES_URL,
                    StatusCode="0",
                    StatusString="删除成功",
                    Id=subscribe_id,
                    LocalTime=datetime.now(tz=CHINA_TZ),
                )
                for subscribe_id in parsed_subscribe_ids
            ]
        )
    )


@router.put(
    path=f"{constants.SUBSCRIBES_URL}/{{subscribe_id}}",
    response_model=ResponseStatus,
    description="GA/T 1400.4-2017 7.2.20.3 取消订阅",
)
async def subscribe_cancel(
    subscribe_id: str,
    data: Subscribe,
    service: Annotated[SubscribeService, Depends(SubscribeService)],
) -> ResponseStatus:
    """处理 7.2.20.3 单条订阅取消。

    路径 `subscribe_id` 是响应状态 ID 和任务定位依据，请求体保留
    协议订阅对象用于更新订阅状态。
    """

    _ = await service.update_subscribe_by_id(
        subscribe_id=subscribe_id,
        subscribe=data,
    )
    return ResponseStatus(
        RequestURL=f"{constants.SUBSCRIBES_URL}/{subscribe_id}",
        StatusCode="0",
        StatusString="取消订阅成功",
        Id=subscribe_id,
        LocalTime=datetime.now(tz=CHINA_TZ),
    )
