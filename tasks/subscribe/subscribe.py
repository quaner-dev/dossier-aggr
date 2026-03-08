import brokers
from collections.abc import Sequence

from models import Subscribe
from repositories.subscribe.subscribe import (
    create_subscribes_repo,
    delete_subscribes_repo,
    get_subscribe_repo,
    list_subscribes_repo,
    update_subscribe_by_id_repo,
    update_subscribes_repo,
)


async def list_subscribes_task() -> Sequence[Subscribe]:
    """查询所有订阅信息"""
    return await list_subscribes_repo()


async def get_subscribe_task(subscribe_id: str) -> Subscribe:
    """根据SubscribeID查询订阅信息"""
    return await get_subscribe_repo(subscribe_id=subscribe_id)


@brokers.broker.task
async def create_subscribes_task(
    subscribes: list[Subscribe],
) -> Sequence[Subscribe]:
    """创建订阅任务"""
    return await create_subscribes_repo(subscribes=subscribes)


@brokers.broker.task
async def update_subscribes_task(
    subscribes: list[Subscribe],
) -> Sequence[Subscribe]:
    """更新订阅任务"""
    return await update_subscribes_repo(subscribes=subscribes)


@brokers.broker.task
async def update_subscribe_by_id_task(
    subscribe_id: str,
    subscribe: Subscribe,
) -> Subscribe:
    """按订阅ID更新单条订阅信息"""
    return await update_subscribe_by_id_repo(
        subscribe_id=subscribe_id,
        subscribe=subscribe,
    )


@brokers.broker.task
async def delete_subscribes_task(
    subscribe_ids: list[str],
) -> None:
    """删除订阅任务"""
    await delete_subscribes_repo(subscribe_ids=subscribe_ids)
