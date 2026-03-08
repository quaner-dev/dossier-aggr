from collections.abc import Sequence
from typing import Any, cast

import exceptions
from database import engine
from models import Archive
from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession


async def list_archives_repo() -> Sequence[Archive]:
    async with AsyncSession(engine) as session:
        archives = (await session.exec(select(Archive))).all()
        if not archives:
            raise exceptions.DataNotFoundError(detail="No Archive data exist")
        return archives


async def create_archives_repo(archives: list[Archive]) -> Sequence[Archive]:
    async with AsyncSession(engine) as session:
        for archive in archives:
            statement = select(Archive).where(Archive.ArchiveID == archive.ArchiveID)
            if (await session.exec(statement)).first():
                raise exceptions.DataAlreadyExistsError(
                    detail=f"{archive.ArchiveID} already exists"
                )
            session.add(archive)

        await session.commit()
        for archive in archives:
            await session.refresh(archive)
    return archives


async def update_archives_repo(archives: list[Archive]) -> Sequence[Archive]:
    async with AsyncSession(engine) as session:
        for archive in archives:
            statement = select(Archive).where(Archive.ArchiveID == archive.ArchiveID)
            if not (await session.exec(statement)).first():
                raise exceptions.DataNotFoundError(detail=f"{archive.ArchiveID} not found")
            session.add(archive)

        await session.commit()
        for archive in archives:
            await session.refresh(archive)
    return archives


async def delete_archives_repo(archive_ids: list[str]) -> list[str]:
    async with AsyncSession(engine) as session:
        _ = await session.exec(delete(Archive).where(cast(Any, Archive.ArchiveID).in_(archive_ids)))
        await session.commit()
    return archive_ids
 
