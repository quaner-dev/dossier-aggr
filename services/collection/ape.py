from sqlmodel import select

from collections.abc import Sequence
from models import APE
import exceptions
from services.common.common import BaseService


class APEService(BaseService):
    """APE服务类，封装APE相关的业务逻辑"""

    async def list_apes(self) -> Sequence[APE]:
        """查询所有APE信息"""
        statement = select(APE)
        apes = (await self.session.exec(statement)).all()
        if not apes:
            raise exceptions.DataNotFoundError(detail="No APE data exist")

        return apes

    async def create_ape(self, ape: APE) -> APE:
        """创建APE设备"""
        self.session.add(ape)
        await self.session.commit()
        await self.session.refresh(ape)
        return ape

    async def create_apes(self, apes: list[APE]) -> Sequence[APE]:
        """批量创建APE设备"""
        for ape in apes:
            self.session.add(ape)
        await self.session.commit()
        for ape in apes:
            await self.session.refresh(ape)
        return apes

    async def update_apes(self, apes: list[APE]) -> Sequence[APE]:
        """批量更新APE设备"""
        for ape in apes:
            self.session.add(ape)
        await self.session.commit()
        for ape in apes:
            await self.session.refresh(ape)
        return apes

    async def delete_ape(self, ape_id: str) -> None:
        """删除APE设备"""
        statement = select(APE).where(APE.ApeID == ape_id)
        ape = (await self.session.exec(statement)).first()
        await self.session.delete(ape)
        await self.session.commit()
