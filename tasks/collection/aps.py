from models import APS
from collections.abc import Sequence
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
import exceptions
from database import engine
from models.common import enums


async def list_apss_task() -> Sequence[APS]:
    async with AsyncSession(engine) as session:
        apss = (await session.exec(select(APS))).all()
        if not apss:
            raise exceptions.DataNotFoundError(detail="No APS data exist")
        return apss


async def update_aps_task(aps_id: str) -> APS:
    async with AsyncSession(engine) as session:
        aps = await session.get(APS, aps_id)
        if not aps:
            raise exceptions.DataNotFoundError(detail=f"{aps_id} not exist")
        aps.IsOnline = enums.StatusTypeEnum.Online
        session.add(aps)
        await session.commit()
        await session.refresh(aps)
        return aps
