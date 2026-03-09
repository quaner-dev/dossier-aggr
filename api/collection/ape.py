from datetime import datetime
from typing import Annotated

from fastapi import Depends, APIRouter

from models import (
    APEList,
    APEListSchema,
    ResponseStatusListSchema,
    ResponseStatus,
    ResponseStatusList,
)
from services import APEService
import constants

router = APIRouter()


@router.get(
    path=constants.APES_URL,
    response_model=APEListSchema,
    description="GA/T 1400.4-2017 7.2.5 采集设备的查询消息",
)
async def apes_query(
    service: Annotated[APEService, Depends(APEService)],
) -> APEListSchema:
    """查询所有APE信息"""
    apes = await service.list_apes()
    return APEListSchema(APEListObject=APEList(APEObject=[ape for ape in apes]))


@router.put(
    path=constants.APES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.5 采集设备的修改消息",
)
async def apes_update(
    data: APEListSchema,
    service: Annotated[APEService, Depends(APEService)],
) -> ResponseStatusListSchema:
    """批量采集设备修改接口"""
    apes = data.APEListObject.APEObject
    _ = await service.update_apes(apes)

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.APES_URL,
                    StatusCode="0",
                    StatusString="修改成功",
                    Id=ape.ApeID,
                    LocalTime=datetime.now(),
                )
                for ape in apes
            ]
        )
    )
