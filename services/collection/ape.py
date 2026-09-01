from domain import APE as APEData
from models import APE
from repo.collection.ape import list_apes_repo, update_apes_repo
from services.model_conversion import to_table_models


class APEService:
    """编排 GA/T 1400 APE 前端设备业务链路。

    APE 查询和低频设备更新直接使用 repo。
    """

    async def list_apes(self) -> list[APE]:
        """查询所有APE信息"""
        return list(await list_apes_repo())

    async def update_apes(self, apes: list[APEData]) -> list[APE]:
        """批量更新APE设备"""
        return await update_apes_repo(apes=to_table_models(APE, apes))
