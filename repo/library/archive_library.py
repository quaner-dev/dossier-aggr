from collections.abc import Mapping, Sequence
from typing import Any, cast

from core import exceptions
from core.database import engine
from models import ArchiveLibrary
from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession
from core.utils import parse_datetime

_FILTERABLE_LIBRARY_FIELDS = {
    "ArchiveLibraryID",
    "Name",
    "CreateTime",
    "Memo",
}


def _normalize_library_filter_value(field: str, value: str):
    if field == "CreateTime":
        return parse_datetime(value)
    return value


async def list_archive_libraries_repo(
    filters: Mapping[str, str] | None = None,
) -> Sequence[ArchiveLibrary]:
    async with AsyncSession(engine) as session:
        statement = select(ArchiveLibrary)
        for field, value in (filters or {}).items():
            if field not in _FILTERABLE_LIBRARY_FIELDS:
                raise exceptions.InvalidParameterError(
                    detail=f"{field} is not a supported query field"
                )
            statement = statement.where(
                getattr(ArchiveLibrary, field)
                == _normalize_library_filter_value(field, value)
            )
        libraries = (await session.exec(statement)).all()
        if not libraries:
            raise exceptions.DataNotFoundError(detail="No ArchiveLibrary data exist")
        return libraries


async def create_archive_libraries_repo(
    libraries: Sequence[ArchiveLibrary],
) -> Sequence[ArchiveLibrary]:
    async with AsyncSession(engine) as session:
        for library in libraries:
            statement = select(ArchiveLibrary).where(
                ArchiveLibrary.ArchiveLibraryID == library.ArchiveLibraryID
            )
            if (await session.exec(statement)).first():
                raise exceptions.DataAlreadyExistsError(
                    detail=f"{library.ArchiveLibraryID} already exists"
                )
            session.add(library)

        await session.commit()
        for library in libraries:
            await session.refresh(library)
    return libraries


async def update_archive_libraries_repo(
    libraries: Sequence[ArchiveLibrary],
) -> Sequence[ArchiveLibrary]:
    async with AsyncSession(engine) as session:
        for library in libraries:
            statement = select(ArchiveLibrary).where(
                ArchiveLibrary.ArchiveLibraryID == library.ArchiveLibraryID
            )
            if not (await session.exec(statement)).first():
                raise exceptions.DataNotFoundError(
                    detail=f"{library.ArchiveLibraryID} not found"
                )
            session.add(library)

        await session.commit()
        for library in libraries:
            await session.refresh(library)
    return libraries


async def delete_archive_libraries_repo(library_ids: list[str]) -> list[str]:
    async with AsyncSession(engine) as session:
        _ = await session.exec(
            delete(ArchiveLibrary).where(
                cast(Any, ArchiveLibrary.ArchiveLibraryID).in_(library_ids)
            )
        )
        await session.commit()
    return library_ids
