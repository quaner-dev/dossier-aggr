from models import Subscribe
from repositories.subscribe.subscribe import get_subscribe_repo, list_subscribes_repo
from tasks import (
    create_subscribes_task,
    update_subscribe_by_id_task,
    update_subscribes_task,
    delete_subscribes_task,
)
from services.task_dispatch import dispatch_and_wait


class SubscribeService:
    async def get_subscribe(self, subscribe_id: str) -> Subscribe:
        """根据SubscribeID查询单条订阅信息"""
        return await get_subscribe_repo(subscribe_id=subscribe_id)

    async def list_subscribes(self) -> list[Subscribe]:
        """查询所有订阅信息"""
        return list(await list_subscribes_repo())

    async def create_subscribes(self, subscribes: list[Subscribe]) -> list[Subscribe]:
        """创建订阅任务"""
        return await dispatch_and_wait(create_subscribes_task, subscribes=subscribes)

    async def update_subscribes(self, subscribes: list[Subscribe]) -> list[Subscribe]:
        """更新订阅信息"""
        return await dispatch_and_wait(update_subscribes_task, subscribes=subscribes)

    async def update_subscribe_by_id(
        self, subscribe_id: str, subscribe: Subscribe
    ) -> Subscribe:
        """按订阅ID更新单条订阅信息"""
        updated = await dispatch_and_wait(
            update_subscribe_by_id_task,
            subscribe_id=subscribe_id,
            subscribe=subscribe,
        )
        return updated

    async def delete_subscribe(self, subscribe_ids: list[str]) -> None:
        """删除订阅信息"""
        _ = await dispatch_and_wait(delete_subscribes_task, subscribe_ids=subscribe_ids)
