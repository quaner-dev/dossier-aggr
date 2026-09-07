from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from core import constants
from core.settings import CHINA_TZ
from domain import ResponseStatus
from schemas import KeepaliveSchema
from services import APSService

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
        LocalTime=datetime.now(tz=CHINA_TZ),
    )
