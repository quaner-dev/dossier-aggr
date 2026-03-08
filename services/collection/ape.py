from collections.abc import Sequence
from models import APE
from repositories.collection.ape import list_apes_repo
from tasks import update_apes_task
from services.task_dispatch import dispatch_and_wait


class APEService:
    """APE服务类，封装APE相关的业务逻辑"""

    async def list_apes(self) -> Sequence[APE]:
        """查询所有APE信息"""
        apes = await list_apes_repo()
        return apes

    async def update_apes(self, apes: list[APE]) -> Sequence[APE]:
        """批量更新APE设备"""
        return await dispatch_and_wait(update_apes_task, apes=apes)
