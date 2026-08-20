from models import APS
from repo.collection.aps import list_apss_repo, update_aps_repo


class APSService:
    """编排 GA/T 1400 APS 平台业务链路。

    APS 查询和注册/保活触发的低频更新直接使用 repo。
    """

    async def list_apss(self) -> list[APS]:
        """查询所有APS信息"""
        return list(await list_apss_repo())

    async def update_aps(self, aps_id: str) -> str:
        """更新APS信息"""
        await update_aps_repo(aps_id=aps_id)
        return aps_id
