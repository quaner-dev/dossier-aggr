from models import Subscribe
from tasks import (
    create_subscribes_task,
    list_subscribes_task,
    update_subscribes_task,
    delete_subscribes_task,
)


class SubscribeService:
    async def list_subscribes(self) -> list[Subscribe]:
        """查询所有订阅信息"""
        return list[Subscribe](await list_subscribes_task())

    async def create_subscribes(self, subscribes: list[Subscribe]) -> list[Subscribe]:
        """创建订阅任务"""
        return await create_subscribes_task.kiq(subscribes=subscribes)

    async def update_subscribes(self, subscribes: list[Subscribe]) -> list[Subscribe]:
        """更新订阅信息"""
        return await update_subscribes_task.kiq(subscribes=subscribes)

    async def delete_subscribe(self, subscribe_ids: list[str]) -> None:
        """删除订阅信息"""
        return await delete_subscribes_task.kiq(subscribe_ids=subscribe_ids)
