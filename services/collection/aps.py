from models import APS
from collections.abc import Sequence
from tasks import list_apss_task


class APSService:
    """APS服务类，封装APS相关的业务逻辑"""

    async def list_apss(self) -> Sequence[APS]:
        """查询所有APS信息"""
        apss = await list_apss_task()
        return apss
