from collections.abc import Sequence
from typing import Any, cast

import exceptions
from database import engine
from models import ArchiveQuery, VehicleArchive
from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession


async def list_vehicle_archives_repo() -> Sequence[VehicleArchive]:
    return await query_vehicle_archives_repo(query=None)


async def query_vehicle_archives_repo(
    query: ArchiveQuery | None,
) -> Sequence[VehicleArchive]:
    async with AsyncSession(engine) as session:
        statement = select(VehicleArchive)
        fields = query.Fields if query else None
        if fields:
            if fields.ArchiveLibraryID:
                statement = statement.where(
                    VehicleArchive.ArchiveLibraryID == fields.ArchiveLibraryID
                )
            if fields.ArchiveIDList:
                statement = statement.where(
                    cast(Any, VehicleArchive.ArchiveID).in_(fields.ArchiveIDList)
                )
            if fields.PlateNos:
                statement = statement.where(
                    cast(Any, VehicleArchive.PlateNo).in_(
                        [plate.strip() for plate in fields.PlateNos.split(",") if plate.strip()]
                    )
                )
            if fields.PlateColor is not None:
                statement = statement.where(VehicleArchive.PlateColor == fields.PlateColor)
            if fields.VehicleClass:
                statement = statement.where(VehicleArchive.VehicleClass == fields.VehicleClass)
            if fields.VehicleBrand is not None:
                statement = statement.where(VehicleArchive.VehicleBrand == fields.VehicleBrand)
            if fields.VehicleModel:
                statement = statement.where(VehicleArchive.VehicleModel == fields.VehicleModel)
            if fields.VehicleColor is not None:
                statement = statement.where(VehicleArchive.VehicleColor == fields.VehicleColor)
            if fields.VehicleStyles:
                statement = statement.where(VehicleArchive.VehicleStyles == fields.VehicleStyles)

        archives = (await session.exec(statement)).all()
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
