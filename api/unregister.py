from datetime import datetime

from fastapi import Depends, APIRouter

import base
import schemas
import services
import constants

router = APIRouter()


@router.post(
    path=constants.UNREGISTER_URL,
    response_model=schemas.ResponseStatus,
    description="GA/T 1400.4-2017 7.2.2 注销消息",
)
async def unregister(
    data: schemas.UnRegisterSchema,
    service: services.APSService = Depends(services.APSService),
):
    """注销接口"""
    device_id = data.UnRegisterObject.DeviceID
    aps = await service.query(device_id)
    await service.update_IsOnline(aps, base.enums.StatusTypeEnum.Offline)

    response_status_object = schemas.ResponseStatus(
        RequestURL=constants.UNREGISTER_URL,
        StatusCode="0",
        StatusString="注销成功",
        LocalTime=datetime.now(),
    )
    return schemas.ResponseStatusList(ResponseStatusObject=response_status_object)
