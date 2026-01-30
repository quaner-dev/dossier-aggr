from collections.abc import Sequence
from models import APE
from tasks import list_ape_task, update_apes_task


class APEService:
    """APE服务类，封装APE相关的业务逻辑"""

    async def list_apes(self) -> Sequence[APE]:
        """查询所有APE信息"""
        apes = await list_ape_task()
        return apes

    async def update_apes(self, apes: list[APE]) -> Sequence[APE]:
        """批量更新APE设备"""
        _ = await update_apes_task.kiq(apes=apes)
        return apes
