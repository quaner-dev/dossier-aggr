from sqlmodel import SQLModel

from domain.library import ArchiveLibrary


class ArchiveLibraryList(SQLModel):
    ArchiveLibraryObject: list[ArchiveLibrary]


class ArchiveLibraryListSchema(SQLModel):
    ArchiveLibraryListObject: ArchiveLibraryList
