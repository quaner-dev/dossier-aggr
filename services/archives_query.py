from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models import Archive
from base import ArchiveBase
from schemas import ArchiveQuery

from database import get_session


class ArchivesQueryService:
    async def list_archives(
        self, archive_query: ArchiveQuery, session: AsyncSession = Depends(get_session)
    ):
        statement = select(Archive).where(**archive_query.model_dump())
        archives = (await session.exec(statement)).all()
        return [ArchiveBase.model_validate(archive) for archive in archives]
