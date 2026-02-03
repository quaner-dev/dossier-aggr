from models import APS
from collections.abc import Sequence
from tasks import list_apss_task, update_aps_task


class APSService:
    """APS服务类，封装APS相关的业务逻辑"""

    async def list_apss(self) -> Sequence[APS]:
        """查询所有APS信息"""
        apss = await list_apss_task()
        return apss

    async def update_aps(self, aps_id: str):
        """更新APS信息"""
        aps = await update_aps_task(aps_id=aps_id)
        return aps
