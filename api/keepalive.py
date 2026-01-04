from datetime import datetime

from fastapi import Depends, APIRouter

import base.enums as enums
import schemas
import services
import constants

router = APIRouter()


@router.post(
    path=constants.KEEPALIVE_URL,
    response_model=schemas.ResponseStatus,
    description="GA/T 1400.4-2017 7.2.3 保活消息",
)
async def keepalive(
    data: schemas.KeepaliveSchema,
    service: services.APSService = Depends(services.APSService),
):
    """保活接口"""
    device_id = data.KeepaliveObject.DeviceID
    aps = await service.query(device_id)
    await service.update_is_online(aps, enums.StatusTypeEnum.Online)

    response_status_object = schemas.ResponseStatus(
        RequestURL=constants.KEEPALIVE_URL,
        StatusCode="0",
        StatusString="保活成功",
        LocalTime=datetime.now(),
    )
    return schemas.ResponseStatusList(ResponseStatusObject=response_status_object)
