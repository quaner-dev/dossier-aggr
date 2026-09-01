from typing import Annotated

from fastapi import APIRouter, Depends

from core import constants
from domain import SystemTime
from services import SystemTimeService

router = APIRouter()


@router.get(
    path=constants.SYSTEM_TIME_URL,
    response_model=SystemTime,
    description="GA/T 1400.4-2017 7.2.4 校时消息",
)
async def system_time(
    service: Annotated[SystemTimeService, Depends(SystemTimeService)],
) -> SystemTime:
    """校时消息接口"""
    return await service.get_system_time()
