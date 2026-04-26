from collections.abc import Sequence
from models import APE
from repo.collection.ape import list_apes_repo
from tasks import update_apes_task
from services.task_dispatch import dispatch_and_wait


class APEService:
    """编排 GA/T 1400 APE 前端设备业务链路。

    APE 列表读取直接使用 repo；更新通过 Taskiq task 写入，
    保持设备资源接口与持久化层之间的异步边界。
    """

    async def list_apes(self) -> Sequence[APE]:
        """查询所有APE信息"""
        apes = await list_apes_repo()
        return apes

    async def update_apes(self, apes: list[APE]) -> Sequence[APE]:
        """批量更新APE设备"""
        return await dispatch_and_wait(update_apes_task, apes=apes)
