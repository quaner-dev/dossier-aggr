from datetime import datetime

from fastapi import Depends, APIRouter

import constants
from models import ResponseStatus, KeepaliveSchema
from services import APSService
from typing import Annotated

router = APIRouter()


@router.post(
    path=constants.KEEPALIVE_URL,
    response_model=ResponseStatus,
    description="GA/T 1400.4-2017 7.2.3 保活消息",
)
async def keepalive(
    data: KeepaliveSchema, service: Annotated[APSService, Depends(APSService)]
) -> ResponseStatus:
    """保活接口"""
    device_id = data.KeepaliveObject.DeviceID
    _ = await service.update_aps(aps_id=device_id)

    return ResponseStatus(
        RequestURL=constants.KEEPALIVE_URL,
        StatusCode="0",
        StatusString="保活成功",
        LocalTime=datetime.now(),
    )
