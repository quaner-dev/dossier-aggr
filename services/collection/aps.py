from sqlmodel import select

from collections.abc import Sequence
from models import APS
from services.common.common import BaseService


class APSService(BaseService):
    """APS服务类，封装APS相关的业务逻辑"""

    async def list_apss(self) -> Sequence[APS]:
        """查询所有APS信息"""
        statement = select(APS)
        apss = (await self.session.exec(statement)).all()
        return apss
