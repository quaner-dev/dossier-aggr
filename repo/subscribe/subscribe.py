from collections.abc import Sequence
from typing import Any, cast

from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from core import exceptions
from core.database import engine
from models import Subscribe


async def list_subscribes_repo() -> Sequence[Subscribe]:
    """查询所有订阅信息"""
    async with AsyncSession(engine) as session:
        subscribes = (await session.exec(select(Subscribe))).all()
        if not subscribes:
            raise exceptions.DataNotFoundError(detail="No Subscribe data exist")
        return subscribes


async def get_subscribe_repo(subscribe_id: str) -> Subscribe:
    """根据SubscribeID查询订阅信息"""
    async with AsyncSession(engine) as session:
        statement = select(Subscribe).where(Subscribe.SubscribeID == subscribe_id)
        subscribe = (await session.exec(statement)).first()
        if not subscribe:
            raise exceptions.DataNotFoundError(detail=f"{subscribe_id} not found")
        return subscribe


async def create_subscribes_repo(subscribes: list[Subscribe]) -> Sequence[Subscribe]:
    """创建订阅任务"""
    async with AsyncSession(engine) as session:
        for subscribe in subscribes:
            statement = select(Subscribe).where(
                Subscribe.SubscribeID == subscribe.SubscribeID
            )
            if (await session.exec(statement)).first():
                raise exceptions.DataAlreadyExistsError(
                    detail=f"{subscribe.SubscribeID} already exists"
                )
            session.add(subscribe)
        await session.commit()
        for subscribe in subscribes:
            await session.refresh(subscribe)
    return subscribes


async def update_subscribes_repo(subscribes: list[Subscribe]) -> Sequence[Subscribe]:
    """更新订阅任务"""
    async with AsyncSession(engine) as session:
        for subscribe in subscribes:
            statement = select(Subscribe).where(
                Subscribe.SubscribeID == subscribe.SubscribeID
            )
            if not (await session.exec(statement)).first():
                raise exceptions.DataNotFoundError(
                    detail=f"{subscribe.SubscribeID} not found"
                )
            session.add(subscribe)

        await session.commit()
        for subscribe in subscribes:
            await session.refresh(subscribe)
    return subscribes


async def update_subscribe_by_id_repo(
    subscribe_id: str, subscribe: Subscribe
) -> Subscribe:
    """按订阅ID更新单条订阅信息"""
    async with AsyncSession(engine) as session:
        statement = select(Subscribe).where(Subscribe.SubscribeID == subscribe_id)
        exists = (await session.exec(statement)).first()
        if not exists:
            raise exceptions.DataNotFoundError(detail=f"{subscribe_id} not found")

        # Path id is authoritative for single-resource update.
        subscribe.SubscribeID = subscribe_id
        session.add(subscribe)
        await session.commit()
        await session.refresh(subscribe)
    return subscribe


async def delete_subscribes_repo(subscribe_ids: list[str]) -> None:
    """删除订阅任务"""
    async with AsyncSession(engine) as session:
        _ = await session.exec(
            delete(Subscribe).where(cast(Any, Subscribe.SubscribeID).in_(subscribe_ids))
        )
        await session.commit()
