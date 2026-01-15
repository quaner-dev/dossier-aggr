from datetime import datetime

from fastapi import Depends, APIRouter

from base.enums import StatusTypeEnum
import constants
from schemas import ResponseStatus, KeepaliveSchema, ResponseStatusList
from services import APSService

router = APIRouter()


@router.post(
    path=constants.KEEPALIVE_URL,
    response_model=ResponseStatus,
    description="GA/T 1400.4-2017 7.2.3 保活消息",
)
async def keepalive(data: KeepaliveSchema, service: APSService = Depends(APSService)):
    """保活接口"""
    device_id = data.KeepaliveObject.DeviceID
    aps = await service.query(device_id)
    await service.update_is_online(aps, StatusTypeEnum.Online)

    response_status_object = ResponseStatus(
        RequestURL=constants.KEEPALIVE_URL,
        StatusCode="0",
        StatusString="保活成功",
        LocalTime=datetime.now(),
    )
    return ResponseStatusList(ResponseStatusObject=response_status_object)
