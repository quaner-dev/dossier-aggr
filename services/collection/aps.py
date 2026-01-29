from sqlmodel import select

from collections.abc import Sequence
from models import APS, enums
from models.collection.aps import APSList
from services.common.common import BaseService


class APSService(BaseService):
    """APS服务类，封装APS相关的业务逻辑"""

    async def get_aps(self, aps_id: str):
        """根据ApsID查询APS信息"""
        statement = select(APS).where(APS.ApsID == aps_id)
        aps = (await self.session.exec(statement)).first()
        return aps

    async def list_aps(self) -> Sequence[APS]:
        """查询所有APS信息"""
        statement = select(APS)
        apss = (await self.session.exec(statement)).all()
        return apss

    async def create_aps(self, aps: APS):
        """创建APS系统"""
        self.session.add(aps)
        await self.session.commit()
        await self.session.refresh(aps)
        return aps

    async def create_apss(self, apss: list[APS]) -> Sequence[APS]:
        """批量创建APS系统"""
        self.session.add_all(apss)
        await self.session.commit()
        for aps in apss:
            await self.session.refresh(aps)
        return apss

    async def update_aps(self, aps: APS) -> APS:
        """更新APS系统"""
        self.session.add(aps)
        await self.session.commit()
        await self.session.refresh(aps)
        return aps

    async def delete_aps(self, aps: APSList) -> None:
        """删除APS系统"""
        await self.session.delete(aps)
        await self.session.commit()

    async def update_is_online(self, aps: APS, status_type: enums.StatusTypeEnum):
        """更新APS在线状态"""
        if not aps.IsOnline != status_type:
            aps.IsOnline = status_type
            self.session.add(aps)
            await self.session.commit()
