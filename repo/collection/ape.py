from collections.abc import Sequence

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core import exceptions
from core.database import engine
from models import APE


async def list_apes_repo() -> Sequence[APE]:
    async with AsyncSession(engine) as session:
        apes = (await session.exec(select(APE))).all()
        if not apes:
            raise exceptions.DataNotFoundError(detail="No APE data exist")
        return apes


async def update_apes_repo(apes: list[APE]) -> list[APE]:
    async with AsyncSession(engine) as session:
        for ape in apes:
            statement = select(APE).where(APE.ApeID == ape.ApeID)
            if not (await session.exec(statement)).first():
                raise exceptions.DataNotFoundError(detail=f"{ape.ApeID} not exist")
            session.add(ape)

        await session.commit()
        for ape in apes:
            await session.refresh(ape)
        return apes
