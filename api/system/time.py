from typing import Annotated

from fastapi import APIRouter, Depends

import constants
from models import SystemTime
from services import SystemTimeService

router = APIRouter()


@router.get(
    path=constants.SYSTEM_TIME_URL,
    response_model=SystemTime,
    description="GA/T 1400.4-2017 7.2.4 系统时间查询",
)
async def system_time(
    service: Annotated[SystemTimeService, Depends(SystemTimeService)],
) -> SystemTime:
    """系统时间查询接口"""
    return await service.get_system_time()
