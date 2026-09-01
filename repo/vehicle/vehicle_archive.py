from collections.abc import Sequence
from typing import Any, cast

from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from core import exceptions
from core.database import engine
from models import VehicleArchive
from schemas import ArchiveQuery


async def list_vehicle_archives_repo() -> Sequence[VehicleArchive]:
    return await query_vehicle_archives_repo(query=None)


async def query_vehicle_archives_repo(
    query: ArchiveQuery | None,
) -> Sequence[VehicleArchive]:
    """按 GA/T 2350.5 B.6 查询车辆档案。

    Repo 层解释车辆可支持的 `Fields` 条件和图像查询 `SubjectID`
    过滤语义；API 层继续负责协议分页字段和响应包装。
    """

    def _picture_subject_ids() -> list[str]:
        if query is None or query.PictureQueryCondition is None:
            return []
        return [
            condition.SubjectID
            for condition in query.PictureQueryCondition.PictureQueryConditionObject
            if condition.SubjectID
        ]

    def _has_overlap(source: list[str] | None, target: list[str]) -> bool:
        return bool(source and target and set(source) & set(target))

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
        picture_subject_ids = _picture_subject_ids()
        if picture_subject_ids:
            archives = [
                archive
                for archive in archives
                if _has_overlap(archive.SourceIDList, picture_subject_ids)
            ]
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
