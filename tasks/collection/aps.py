from models import APS
from collections.abc import Sequence
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
import exceptions
from database import engine


async def list_apss_task() -> Sequence[APS]:
    async with AsyncSession(engine) as session:
        apss = (await session.exec(select(APS))).all()
        if not apss:
            raise exceptions.DataNotFoundError(detail="No APS data exist")
        return apss
