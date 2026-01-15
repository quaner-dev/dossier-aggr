from typing import List

from sqlmodel import select

import base
from models import APS
import exceptions
from .common import BaseService


class APSService(BaseService):
    """APS服务类，封装APS相关的业务逻辑"""

    async def query(self, device_id: str):
        """根据设备ID查询APS信息"""
        statement = select(APS).where(APS.ApsID == device_id)
        aps = (await self.session.exec(statement)).first()
        if not aps:
            raise exceptions.DataNotFoundError(detail=f"{device_id} not exist")
        return aps

    async def get_aps(self, aps_id: str) -> base.aps.APSBase:
        """根据ApsID查询APS信息"""
        statement = select(APS).where(APS.ApsID == aps_id)
        aps = (await self.session.exec(statement)).first()
        if not aps:
            raise exceptions.DataNotFoundError(detail=f"{aps_id} not exist")
        return base.aps.APSBase.model_validate(aps)

    async def list_aps(self) -> List[base.aps.APSBase]:
        """查询所有APS信息"""
        statement = select(APS)
        aps_list = (await self.session.exec(statement)).all()
        if not aps_list:
            raise exceptions.DataNotFoundError(detail="No APS data exist")
        return [base.aps.APSBase.model_validate(aps) for aps in aps_list]

    async def create_aps(self, aps: base.aps.APSBase) -> APS:
        """创建APS系统"""
        db_aps = APS.model_validate(aps)
        self.session.add(db_aps)
        await self.session.commit()
        await self.session.refresh(db_aps)
        return db_aps

    async def batch_create_aps(self, aps_list: List[base.aps.APSBase]) -> List[APS]:
        """批量创建APS系统"""
        db_aps_list = [APS.model_validate(aps) for aps in aps_list]
        for db_aps in db_aps_list:
            self.session.add(db_aps)
        await self.session.commit()
        for db_aps in db_aps_list:
            await self.session.refresh(db_aps)
        return db_aps_list

    async def update_aps(self, aps_id: str, aps: base.aps.APSBase) -> APS:
        """更新APS系统"""
        statement = select(APS).where(APS.ApsID == aps_id)
        db_aps = (await self.session.exec(statement)).first()
        if not db_aps:
            raise exceptions.DataNotFoundError(detail=f"{aps_id} not exist")
        
        for key, value in aps.model_dump(exclude={"id"}).items():
            setattr(db_aps, key, value)
        
        self.session.add(db_aps)
        await self.session.commit()
        await self.session.refresh(db_aps)
        return db_aps

    async def delete_aps(self, aps_id: str) -> None:
        """删除APS系统"""
        statement = select(APS).where(APS.ApsID == aps_id)
        db_aps = (await self.session.exec(statement)).first()
        if not db_aps:
            raise exceptions.DataNotFoundError(detail=f"{aps_id} not exist")
        
        await self.session.delete(db_aps)
        await self.session.commit()

    async def update_is_online(self, aps: APS, status_type: base.enums.StatusTypeEnum):
        """更新APS在线状态"""
        if not aps.IsOnline != status_type:
            aps.IsOnline = status_type
            self.session.add(aps)
            await self.session.commit()
