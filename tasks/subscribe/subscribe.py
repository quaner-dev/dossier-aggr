import brokers
from models import Subscribe
from sqlmodel.ext.asyncio.session import AsyncSession
from database import engine
from collections.abc import Sequence
import exceptions
from sqlmodel import select, delete


async def list_subscribes_task() -> Sequence[Subscribe]:
    """查询所有订阅信息"""
    async with AsyncSession(engine) as session:
        subscribes = (await session.exec(select(Subscribe))).all()
        if not subscribes:
            raise exceptions.DataNotFoundError(detail="No Subscribe data exist")
        return subscribes


@brokers.broker.task
async def create_subscribes_task(
    subscribes: list[Subscribe],
) -> Sequence[Subscribe]:
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


@brokers.broker.task
async def update_subscribes_task(
    subscribes: list[Subscribe],
) -> Sequence[Subscribe]:
    """更新订阅任务"""
    async with AsyncSession(engine) as session:
        session.add_all(subscribes)
        await session.commit()
        await session.refresh(subscribes)
    return subscribes


@brokers.broker.task
async def delete_subscribes_task(
    subscribe_ids: list[str],
) -> None:
    """删除订阅任务"""
    async with AsyncSession(engine) as session:
        _ = await session.exec(
            delete(Subscribe).where(Subscribe.SubscribeID.in_(subscribe_ids))
        )
        await session.commit()
