import asyncio
from collections.abc import Sequence
from typing import Any, cast

from core import exceptions
from core.database import engine
from models import ArchiveSubject
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

_TABLE_INIT_LOCK = asyncio.Lock()
_TABLE_READY = False


async def _ensure_table() -> None:
    global _TABLE_READY
    if _TABLE_READY:
        return

    async with _TABLE_INIT_LOCK:
        if _TABLE_READY:
            return
        async with engine.begin() as conn:
            table = cast(Any, ArchiveSubject).__table__
            await conn.run_sync(
                SQLModel.metadata.create_all,
                tables=[table],
            )
        _TABLE_READY = True


async def query_archive_subjects_repo() -> Sequence[ArchiveSubject]:
    await _ensure_table()
    async with AsyncSession(engine) as session:
        subjects = (await session.exec(select(ArchiveSubject))).all()
        if not subjects:
            raise exceptions.DataNotFoundError(detail="No ArchiveSubject data exist")
        return subjects


async def create_archive_subjects_repo(
    subjects: list[ArchiveSubject],
) -> Sequence[ArchiveSubject]:
    await _ensure_table()
    async with AsyncSession(engine) as session:
        for subject in subjects:
            statement = select(ArchiveSubject).where(
                ArchiveSubject.ArchiveID == subject.ArchiveID
            )
            if (await session.exec(statement)).first():
                raise exceptions.DataAlreadyExistsError(
                    detail=f"{subject.ArchiveID} already exists"
                )
            session.add(subject)

        await session.commit()
        for subject in subjects:
            await session.refresh(subject)
    return subjects


async def update_archive_subjects_repo(
    subjects: list[ArchiveSubject],
) -> Sequence[ArchiveSubject]:
    await _ensure_table()
    async with AsyncSession(engine) as session:
        for subject in subjects:
            statement = select(ArchiveSubject).where(
                ArchiveSubject.ArchiveID == subject.ArchiveID
            )
            if not (await session.exec(statement)).first():
                raise exceptions.DataNotFoundError(detail=f"{subject.ArchiveID} not found")
            session.add(subject)

        await session.commit()
        for subject in subjects:
            await session.refresh(subject)
    return subjects


async def delete_archive_subjects_repo(
    archive_id: str,
) -> list[str]:
    await _ensure_table()
    async with AsyncSession(engine) as session:
        statement = select(ArchiveSubject).where(ArchiveSubject.ArchiveID == archive_id)
        subject = (await session.exec(statement)).first()

        if subject:
            await session.delete(subject)
            await session.commit()
            return [archive_id]

    return []
