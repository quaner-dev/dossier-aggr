from collections.abc import Sequence

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core import exceptions
from core.database import engine
from domain.common import enums
from models import APS


async def list_apss_repo() -> Sequence[APS]:
    async with AsyncSession(engine) as session:
        apss = (await session.exec(select(APS))).all()
        if not apss:
            raise exceptions.DataNotFoundError(detail="No APS data exist")
        return apss


async def update_aps_repo(aps_id: str) -> APS:
    async with AsyncSession(engine) as session:
        statement = select(APS).where(APS.ApsID == aps_id)
        aps = (await session.exec(statement)).first()
        if not aps:
            raise exceptions.DataNotFoundError(detail=f"{aps_id} not exist")
        aps.IsOnline = enums.StatusTypeEnum.Online
        session.add(aps)
        await session.commit()
        await session.refresh(aps)
        return aps
