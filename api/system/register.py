from datetime import datetime
from typing import Annotated

from fastapi import Depends, Request, APIRouter

import auth

from models import ResponseStatusList, ResponseStatus, RegisterSchema
from services import APSService
import constants

router = APIRouter()
security = auth.HTTPDigest1400()


@router.post(
    path=constants.REGISTER_URL,
    response_model=ResponseStatusList,
    dependencies=[Depends(security)],
    description="GA/T 1400.4-2017 7.2.1 注册消息",
)
async def register(
    request: Request,
    data: RegisterSchema,
    service: Annotated[APSService, Depends(APSService)],
):
    """注册接口"""
    device_id = data.RegisterObject.DeviceID
    _ = await service.update_aps(aps_id=device_id)

    # TODO 这里是硬编码，需要后期将输出的方法整体迁移到固定位置，防止反复描述
    return ResponseStatusList(
        ResponseStatusObject=[
            ResponseStatus(
                RequestURL=str(request.url),
                StatusCode="0",
                StatusString="注册成功",
                LocalTime=datetime.now(),
            )
        ]
    )
