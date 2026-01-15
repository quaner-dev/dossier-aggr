from datetime import datetime

from fastapi import Depends, APIRouter, Query

from schemas import (
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
    response_model=APEList,
    description="GA/T 1400.4-2017 7.2.5 采集设备的查询（单个设备）",
)
async def get_ape(
    ape_id: str = Query(..., alias="ApeID", max_length=20),
    service: APEService = Depends(APEService),
):
    """根据APE ID查询APE信息"""
    ape = await service.get_ape(ape_id)
    return APEList(APEObject=[ape])


@router.get(
    path=constants.APES_URL,
    response_model=APEListSchema,
    description="GA/T 1400.4-2017 7.2.5 采集设备的查询",
)
async def list_apes(service: APEService = Depends(APEService)):
    """查询所有APE信息"""
    apes = await service.list_apes()
    return APEListSchema(APEListObject=APEList(APEObject=apes))


@router.post(
    path=constants.APES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.6.1 批量采集设备增加",
)
async def apes_create(
    data: APEListSchema,
    service: APEService = Depends(APEService),
):
    """批量采集设备增加接口"""
    apes = data.APEListObject.APEObject
    await service.batch_create_apes(apes)

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.APES_URL,
            StatusCode="0",
            StatusString="上传成功",
            Id=ape.ApeID,
            LocalTime=datetime.now(),
        )
        for ape in apes
    ]

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )


@router.put(
    path=constants.APES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.6.2 批量采集设备修改",
)
async def apes_update(
    data: APEListSchema,
    service: APEService = Depends(APEService),
):
    """批量采集设备修改接口"""
    apes = data.APEListObject.APEObject
    for ape in apes:
        await service.update_ape(ape.ApeID, ape)

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.APES_URL,
            StatusCode="0",
            StatusString="修改成功",
            Id=ape.ApeID,
            LocalTime=datetime.now(),
        )
        for ape in apes
    ]

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )


@router.delete(
    path=constants.APES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.6.3 批量采集设备删除",
)
async def apes_delete(
    id_list: str = Query(..., alias="IDList"),
    service: APEService = Depends(APEService),
):
    """批量采集设备删除接口"""
    ape_ids = [id.strip() for id in id_list.split(",")]
    
    for ape_id in ape_ids:
        await service.delete_ape(ape_id)

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.APES_URL,
            StatusCode="0",
            StatusString="删除成功",
            Id=ape_id,
            LocalTime=datetime.now(),
        )
        for ape_id in ape_ids
    ]

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )
