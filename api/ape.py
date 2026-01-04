from fastapi import Depends, APIRouter, Query

import schemas
from services import APEService
import constants

router = APIRouter()


@router.get(
    path=constants.APES_URL,
    response_model=schemas.ape.APEListSchema,
    description="GA/T 1400.4-2017 7.2.5 采集设备的查询",
)
async def apes_read(service: APEService = Depends(APEService)):
    """查询所有APE信息"""
    apes = await service.list_apes()
    return schemas.ape.APEListSchema(APEListObject=schemas.ape.APEList(APEObject=apes))


@router.get(
    path=constants.APES_URL,
    response_model=schemas.APEList,
    description="GA/T 1400.4-2017 7.2.5 采集设备的查询（单个设备）",
)
async def ape_read(
    ape_id: str = Query(max_length=20),
    service: APEService = Depends(APEService),
):
    """根据APE ID查询APE信息"""
    ape = await service.get_ape(ape_id)
    return schemas.APEList(APEObject=[ape])
