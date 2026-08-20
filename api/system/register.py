from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Request

from core import auth, constants
from core.time import CHINA_TZ
from models import RegisterSchema, ResponseStatus, ResponseStatusList
from services import APSService

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
    """处理 7.2.1 注册消息并返回单项状态。"""

    device_id = data.RegisterObject.DeviceID
    _ = await service.update_aps(aps_id=device_id)

    # 注册成功语义固定，当前接口不暴露额外业务错误映射。
    return ResponseStatusList(
        ResponseStatusObject=[
            ResponseStatus(
                RequestURL=str(request.url),
                StatusCode="0",
                StatusString="注册成功",
                LocalTime=datetime.now(tz=CHINA_TZ),
            )
        ]
    )
