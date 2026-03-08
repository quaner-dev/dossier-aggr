from collections.abc import Sequence
from typing import Any, cast

import exceptions
from database import engine
from models import VehicleArchive
from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession


async def list_vehicle_archives_repo() -> Sequence[VehicleArchive]:
    async with AsyncSession(engine) as session:
        archives = (await session.exec(select(VehicleArchive))).all()
        if not archives:
            raise exceptions.DataNotFoundError(detail="No VehicleArchive data exist")
        return archives


async def create_vehicle_archives_repo(
    archives: list[VehicleArchive],
) -> Sequence[VehicleArchive]:
    async with AsyncSession(engine) as session:
        for archive in archives:
            statement = select(VehicleArchive).where(
                VehicleArchive.ArchiveID == archive.ArchiveID
            )
            if (await session.exec(statement)).first():
                raise exceptions.DataAlreadyExistsError(
                    detail=f"{archive.ArchiveID} already exists"
                )
            session.add(archive)

        await session.commit()
        for archive in archives:
            await session.refresh(archive)
    return archives


async def update_vehicle_archives_repo(
    archives: list[VehicleArchive],
) -> Sequence[VehicleArchive]:
    async with AsyncSession(engine) as session:
        for archive in archives:
            statement = select(VehicleArchive).where(
                VehicleArchive.ArchiveID == archive.ArchiveID
            )
            if not (await session.exec(statement)).first():
                raise exceptions.DataNotFoundError(detail=f"{archive.ArchiveID} not found")
            session.add(archive)

        await session.commit()
        for archive in archives:
            await session.refresh(archive)
    return archives


async def delete_vehicle_archives_repo(archive_ids: list[str]) -> list[str]:
    async with AsyncSession(engine) as session:
        _ = await session.exec(
            delete(VehicleArchive).where(
                cast(Any, VehicleArchive.ArchiveID).in_(archive_ids)
            )
        )
        await session.commit()
    return archive_ids
