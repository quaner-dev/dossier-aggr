from collections.abc import Sequence
from typing import Any, cast

from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from core import exceptions
from core.database import engine
from models import Archive, ArchiveQuery


async def list_archives_repo() -> Sequence[Archive]:
    return await query_archives_repo(query=None)


async def query_archives_repo(
    query: ArchiveQuery | None,
) -> Sequence[Archive]:
    """按 GA/T 2350.5 B.6 查询人员档案。

    Repo 层负责解释当前支持的 `Fields` 和 `PictureQueryCondition.SubjectID`
    过滤语义；分页仍由 API 层按协议响应包装裁剪，避免数据访问层混入
    HTTP 响应结构。
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
        statement = select(Archive)
        fields = query.Fields if query else None
        if fields:
            if fields.ArchiveLibraryID:
                statement = statement.where(Archive.ArchiveLibraryID == fields.ArchiveLibraryID)
            if fields.ArchiveIDList:
                statement = statement.where(
                    cast(Any, Archive.ArchiveID).in_(fields.ArchiveIDList)
                )

        archives = (await session.exec(statement)).all()
        picture_subject_ids = _picture_subject_ids()
        if picture_subject_ids:
            archives = [
                archive
                for archive in archives
                if _has_overlap(archive.SourceIDList, picture_subject_ids)
            ]
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
 
