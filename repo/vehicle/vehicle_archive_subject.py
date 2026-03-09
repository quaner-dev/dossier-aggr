import asyncio
from collections.abc import Sequence
from typing import Any, cast

import exceptions
from database import engine
from models import VehicleArchiveSubject
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
            table = cast(Any, VehicleArchiveSubject).__table__
            await conn.run_sync(
                SQLModel.metadata.create_all,
                tables=[table],
            )
        _TABLE_READY = True


async def query_vehicle_archive_subjects_repo() -> Sequence[VehicleArchiveSubject]:
    await _ensure_table()
    async with AsyncSession(engine) as session:
        subjects = (await session.exec(select(VehicleArchiveSubject))).all()
        if not subjects:
            raise exceptions.DataNotFoundError(detail="No VehicleArchiveSubject data exist")
        return subjects


async def create_vehicle_archive_subjects_repo(
    subjects: list[VehicleArchiveSubject],
) -> Sequence[VehicleArchiveSubject]:
    await _ensure_table()
    async with AsyncSession(engine) as session:
        for subject in subjects:
            statement = select(VehicleArchiveSubject).where(
                VehicleArchiveSubject.ArchiveID == subject.ArchiveID
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


async def update_vehicle_archive_subjects_repo(
    subjects: list[VehicleArchiveSubject],
) -> Sequence[VehicleArchiveSubject]:
    await _ensure_table()
    async with AsyncSession(engine) as session:
        for subject in subjects:
            statement = select(VehicleArchiveSubject).where(
                VehicleArchiveSubject.ArchiveID == subject.ArchiveID
            )
            if not (await session.exec(statement)).first():
                raise exceptions.DataNotFoundError(detail=f"{subject.ArchiveID} not found")
            session.add(subject)

        await session.commit()
        for subject in subjects:
            await session.refresh(subject)
    return subjects


async def delete_vehicle_archive_subjects_repo(archive_ids: list[str]) -> list[str]:
    await _ensure_table()
    async with AsyncSession(engine) as session:
        deleted_ids: list[str] = []
        for archive_id in archive_ids:
            statement = select(VehicleArchiveSubject).where(
                VehicleArchiveSubject.ArchiveID == archive_id
            )
            subject = (await session.exec(statement)).first()
            if subject:
                await session.delete(subject)
                deleted_ids.append(archive_id)

        if deleted_ids:
            await session.commit()
    return deleted_ids
