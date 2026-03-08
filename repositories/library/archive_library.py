from collections.abc import Sequence
from typing import Any, cast

import exceptions
from database import engine
from models import ArchiveLibrary
from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession


async def list_archive_libraries_repo() -> Sequence[ArchiveLibrary]:
    async with AsyncSession(engine) as session:
        libraries = (await session.exec(select(ArchiveLibrary))).all()
        if not libraries:
            raise exceptions.DataNotFoundError(detail="No ArchiveLibrary data exist")
        return libraries


async def create_archive_libraries_repo(
    libraries: list[ArchiveLibrary],
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
    libraries: list[ArchiveLibrary],
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
