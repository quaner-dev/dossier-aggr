from datetime import datetime

from fastapi import Depends, APIRouter, Query

from schemas import (
    APSList,
    APSListSchema,
    ResponseStatusListSchema,
    ResponseStatus,
    ResponseStatusList,
)
from services import APSService
import constants

router = APIRouter()


@router.get(
    path=constants.APS_URL,
    response_model=APSList,
    description="GA/T 1400.4-2017 7.2.4 采集系统的查询（单个系统）",
)
async def get_aps(
    aps_id: str = Query(..., alias="ApsID", max_length=20),
    service: APSService = Depends(APSService),
):
    """根据APS ID查询APS信息"""
    aps = await service.get_aps(aps_id)
    return APSList(APSObject=[aps])


@router.get(
    path=constants.APS_URL,
    response_model=APSListSchema,
    description="GA/T 1400.4-2017 7.2.4 采集系统的查询",
)
async def list_aps(service: APSService = Depends(APSService)):
    """查询所有APS信息"""
    aps_list = await service.list_aps()
    return APSListSchema(APSListObject=APSList(APSObject=aps_list))


@router.post(
    path=constants.APS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.7.1 批量采集系统增加",
)
async def aps_create(
    data: APSListSchema,
    service: APSService = Depends(APSService),
):
    """批量采集系统增加接口"""
    aps_list = data.APSListObject.APSObject
    await service.batch_create_aps(aps_list)

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.APS_URL,
            StatusCode="0",
            StatusString="上传成功",
            Id=aps.ApsID,
            LocalTime=datetime.now(),
        )
        for aps in aps_list
    ]

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )


@router.put(
    path=constants.APS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.7.2 批量采集系统修改",
)
async def aps_update(
    data: APSListSchema,
    service: APSService = Depends(APSService),
):
    """批量采集系统修改接口"""
    aps_list = data.APSListObject.APSObject
    for aps in aps_list:
        await service.update_aps(aps.ApsID, aps)

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.APS_URL,
            StatusCode="0",
            StatusString="修改成功",
            Id=aps.ApsID,
            LocalTime=datetime.now(),
        )
        for aps in aps_list
    ]

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )


@router.delete(
    path=constants.APS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.7.3 批量采集系统删除",
)
async def aps_delete(
    id_list: str = Query(..., alias="IDList"),
    service: APSService = Depends(APSService),
):
    """批量采集系统删除接口"""
    aps_ids = [id.strip() for id in id_list.split(",")]
    
    for aps_id in aps_ids:
        await service.delete_aps(aps_id)

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.APS_URL,
            StatusCode="0",
            StatusString="删除成功",
            Id=aps_id,
            LocalTime=datetime.now(),
        )
        for aps_id in aps_ids
    ]

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )
