from domain import Subscribe as SubscribeData
from models import Subscribe
from repo.subscribe.subscribe import (
    create_subscribes_repo,
    delete_subscribes_repo,
    get_subscribe_repo,
    list_subscribes_repo,
    update_subscribe_by_id_repo,
    update_subscribes_repo,
)
from services.model_conversion import to_table_model, to_table_models


class SubscribeService:
    """编排 GA/T 1400.4 7.2.20 订阅任务业务链路。

    订阅是需要立即生效的低频控制数据，读写直接委托 repo。
    """

    async def get_subscribe(self, subscribe_id: str) -> Subscribe:
        """根据SubscribeID查询单条订阅信息"""
        return await get_subscribe_repo(subscribe_id=subscribe_id)

    async def list_subscribes(self) -> list[Subscribe]:
        """查询所有订阅信息"""
        return list(await list_subscribes_repo())

    async def create_subscribes(self, subscribes: list[SubscribeData]) -> list[Subscribe]:
        """创建订阅任务"""
        return list(await create_subscribes_repo(subscribes=to_table_models(Subscribe, subscribes)))

    async def update_subscribes(self, subscribes: list[SubscribeData]) -> list[Subscribe]:
        """更新订阅信息"""
        return list(await update_subscribes_repo(subscribes=to_table_models(Subscribe, subscribes)))

    async def update_subscribe_by_id(
        self, subscribe_id: str, subscribe: SubscribeData
    ) -> Subscribe:
        """按订阅ID更新单条订阅信息"""
        return await update_subscribe_by_id_repo(
            subscribe_id=subscribe_id,
            subscribe=to_table_model(Subscribe, subscribe),
        )

    async def delete_subscribe(self, subscribe_ids: list[str]) -> None:
        """删除订阅信息"""
        await delete_subscribes_repo(subscribe_ids=subscribe_ids)
