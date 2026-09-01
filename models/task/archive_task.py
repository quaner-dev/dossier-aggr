from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from domain.task.archive_task import ArchiveTask as ArchiveTaskDomain


class ArchiveTask(ArchiveTaskDomain, table=True):
    __table_args__ = (UniqueConstraint("TaskID"),)

    id: int | None = Field(default=None, primary_key=True, exclude=True)
