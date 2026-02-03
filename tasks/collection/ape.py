import brokers
from models import APE
from collections.abc import Sequence
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
import exceptions
from database import engine


async def list_apes_task() -> Sequence[APE]:
    async with AsyncSession(engine) as session:
        apes = (await session.exec(select(APE))).all()
        if not apes:
            raise exceptions.DataNotFoundError(detail="No APE data exist")
        return apes


@brokers.broker.task
async def update_apes_task(apes: list[APE]):
    async with AsyncSession(engine) as session:
        session.add_all(apes)
        await session.commit()
        await session.refresh(apes)
        return apes
