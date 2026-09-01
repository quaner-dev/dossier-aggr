from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from domain.library.archive_library import ArchiveLibrary as ArchiveLibraryDomain


class ArchiveLibrary(ArchiveLibraryDomain, table=True):
    __table_args__ = (UniqueConstraint("ArchiveLibraryID"),)

    id: int | None = Field(default=None, primary_key=True, exclude=True)
