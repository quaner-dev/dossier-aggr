from models import APS
from collections.abc import Sequence
from repo.collection.aps import list_apss_repo
from tasks import update_aps_task
from services.task_dispatch import dispatch_and_wait


class APSService:
    """编排 GA/T 1400 APS 平台业务链路。

    APS 列表读取直接使用 repo；更新通过 Taskiq task 写入，
    保持系统资源接口与持久化层之间的异步边界。
    """

    async def list_apss(self) -> Sequence[APS]:
        """查询所有APS信息"""
        apss = await list_apss_repo()
        return apss

    async def update_aps(self, aps_id: str):
        """更新APS信息"""
        _ = await dispatch_and_wait(update_aps_task, aps_id=aps_id)
        return aps_id
