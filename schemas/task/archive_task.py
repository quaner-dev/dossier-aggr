from sqlmodel import SQLModel

from domain.task import ArchiveTask


class ArchiveTaskList(SQLModel):
    ArchiveTaskObject: list[ArchiveTask]


class ArchiveTaskListSchema(SQLModel):
    ArchiveTaskListObject: ArchiveTaskList
