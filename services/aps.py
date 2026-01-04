from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

import base
from models.aps import APS
import exceptions
from database import get_session


class APSService:
    """APS服务类，封装APS相关的业务逻辑"""

    async def query(self, device_id: str, session: AsyncSession = Depends(get_session)):
        """根据设备ID查询APS信息"""
        statement = select(APS).where(APS.ApsID == device_id)
        aps = (await session.exec(statement)).first()
        if not aps:
            raise exceptions.DataNotFoundError(detail=f"{device_id} not exist")
        return aps

    async def update_is_online(
        self,
        aps: APS,
        status_type: base.enums.StatusTypeEnum,
        session: AsyncSession = Depends(get_session),
    ):
        """更新APS在线状态"""
        if not aps.IsOnline != status_type:
            aps.IsOnline = status_type
            session.add(aps)
            await session.commit()
