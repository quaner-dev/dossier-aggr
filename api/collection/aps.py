from typing import Annotated

from fastapi import Depends, APIRouter

from models import (
    APSList,
    APSListSchema,
)
from services import APSService
from core import constants

router = APIRouter()


@router.get(
    path=constants.APS_URL,
    response_model=APSListSchema,
    description="GA/T 1400.4-2017 7.2.6 采集系统查询",
)
async def apss_query(
    service: Annotated[APSService, Depends(APSService)],
) -> APSListSchema:
    """查询所有APS信息"""
    apss = await service.list_apss()
    return APSListSchema(APSListObject=APSList(APSObject=[aps for aps in apss]))
