import asyncio
from collections.abc import Sequence
from typing import Any, cast

import exceptions
from database import engine
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
    archive_id: str | None,
    face_id_list: list[str] | None,
    person_id_list: list[str] | None,
    motor_vehicle_id_list: list[str] | None,
    non_motor_vehicle_id_list: list[str] | None,
) -> list[str]:
    # ArchiveSubject has no vehicle id fields; keep params for protocol compatibility.
    _ = motor_vehicle_id_list, non_motor_vehicle_id_list

    await _ensure_table()
    async with AsyncSession(engine) as session:
        all_subjects = (await session.exec(select(ArchiveSubject))).all()

        face_ids = set(face_id_list or [])
        person_ids = set(person_id_list or [])

        def _matched(subject: ArchiveSubject) -> bool:
            if archive_id and subject.ArchiveID != archive_id:
                return False
            if face_ids and not face_ids.intersection(subject.FaceIDList or []):
                return False
            if person_ids and not person_ids.intersection(subject.PersonIDList or []):
                return False
            return True

        matched_subjects = [subject for subject in all_subjects if _matched(subject)]
        deleted_ids = [subject.ArchiveID for subject in matched_subjects]

        for subject in matched_subjects:
            await session.delete(subject)

        if matched_subjects:
            await session.commit()

    return deleted_ids
