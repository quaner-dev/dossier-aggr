from datetime import datetime
from typing import Annotated

from fastapi import Depends, APIRouter

from models import enums, UnRegisterSchema, ResponseStatus, ResponseStatusList
import constants
from services import APSService

router = APIRouter()


@router.post(
    path=constants.UNREGISTER_URL,
    response_model=ResponseStatus,
    description="GA/T 1400.4-2017 7.2.2 注销消息",
)
async def unregister(
    data: UnRegisterSchema, service: Annotated[APSService, Depends(APSService)]
):
    """注销接口"""
    device_id = data.UnRegisterObject.DeviceID
    aps = await service.query(device_id)
    await service.update_is_online(aps, enums.StatusTypeEnum.Offline)

    response_status_object = ResponseStatus(
        RequestURL=constants.UNREGISTER_URL,
        StatusCode="0",
        StatusString="注销成功",
        LocalTime=datetime.now(),
    )
    return ResponseStatusList(ResponseStatusObject=response_status_object)
