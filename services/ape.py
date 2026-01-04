from typing import List

from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from base import APEBase
from models.ape import APE
import exceptions

from database import get_session


class APEService:
    """APE服务类，封装APE相关的业务逻辑"""

    async def get_ape(
        self,
        ape_id: str,
        session: AsyncSession = Depends(get_session),
    ) -> APEBase:
        """根据设备ID查询APE信息"""
        statement = select(APE).where(APE.ApeID == ape_id)
        ape = (await session.exec(statement)).first()
        if not ape:
            raise exceptions.DataNotFoundError(detail=f"{ape_id} not exist")
        return APEBase.model_validate(ape)

    async def list_apes(
        self, session: AsyncSession = Depends(get_session)
    ) -> List[APEBase]:
        """查询所有APE信息"""
        statement = select(APE)
        apes = (await session.exec(statement)).all()
        if not apes:
            raise exceptions.DataNotFoundError(detail="No APE data exist")
        return [APEBase.model_validate(ape) for ape in apes]
