
from sqlmodel import select

from models import APE
import exceptions
from services.common.common import BaseService


class APEService(BaseService):
    """APE服务类，封装APE相关的业务逻辑"""

    async def get_ape(self, ape_id: str) -> APE:
        """根据设备ID查询APE信息"""
        statement = select(APE).where(APE.ApeID == ape_id)
        ape = (await self.session.exec(statement)).first()
        if not ape:
            raise exceptions.DataNotFoundError(detail=f"{ape_id} not exist")
        return APE.model_validate(ape)

    async def list_apes(self) -> list[APE]:
        """查询所有APE信息"""
        statement = select(APE)
        apes = (await self.session.exec(statement)).all()
        if not apes:
            raise exceptions.DataNotFoundError(detail="No APE data exist")
        return [APE.model_validate(ape) for ape in apes]

    async def create_ape(self, ape: APE) -> APE:
        """创建APE设备"""
        db_ape = APE.model_validate(ape)
        self.session.add(db_ape)
        await self.session.commit()
        await self.session.refresh(db_ape)
        return db_ape

    async def batch_create_apes(self, apes: list[APE]) -> list[APE]:
        """批量创建APE设备"""
        db_apes = [APE.model_validate(ape) for ape in apes]
        for db_ape in db_apes:
            self.session.add(db_ape)
        await self.session.commit()
        for db_ape in db_apes:
            await self.session.refresh(db_ape)
        return db_apes

    async def update_ape(self, ape_id: str, ape: APE) -> APE:
        """更新APE设备"""
        statement = select(APE).where(APE.ApeID == ape_id)
        db_ape = (await self.session.exec(statement)).first()
        if not db_ape:
            raise exceptions.DataNotFoundError(detail=f"{ape_id} not exist")
        
        for key, value in ape.model_dump(exclude={"id"}).items():
            setattr(db_ape, key, value)
        
        self.session.add(db_ape)
        await self.session.commit()
        await self.session.refresh(db_ape)
        return db_ape

    async def delete_ape(self, ape_id: str) -> None:
        """删除APE设备"""
        statement = select(APE).where(APE.ApeID == ape_id)
        db_ape = (await self.session.exec(statement)).first()
        if not db_ape:
            raise exceptions.DataNotFoundError(detail=f"{ape_id} not exist")
        
        await self.session.delete(db_ape)
        await self.session.commit()
