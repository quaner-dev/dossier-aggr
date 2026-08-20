from collections.abc import Mapping, Sequence
from typing import Any, cast

from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from core import exceptions
from core.database import engine
from core.utils import parse_datetime
from models import ArchiveTask

_FILTERABLE_TASK_FIELDS = {
    "TaskID",
    "TaskName",
    "ArchiveLibraryID",
    "EventType",
    "Status",
    "CreateTime",
    "UpdateTime",
}


def _normalize_task_filter_value(field: str, value: str):
    if field in {"CreateTime", "UpdateTime"}:
        return parse_datetime(value)
    return value


async def list_archive_tasks_repo(
    filters: Mapping[str, str] | None = None,
) -> Sequence[ArchiveTask]:
    async with AsyncSession(engine) as session:
        statement = select(ArchiveTask)
        for field, value in (filters or {}).items():
            if field not in _FILTERABLE_TASK_FIELDS:
                raise exceptions.InvalidParameterError(
                    detail=f"{field} is not a supported query field"
                )
            statement = statement.where(
                getattr(ArchiveTask, field) == _normalize_task_filter_value(field, value)
            )
        tasks = (await session.exec(statement)).all()
        if not tasks:
            raise exceptions.DataNotFoundError(detail="No ArchiveTask data exist")
        return tasks


async def create_archive_tasks_repo(
    tasks: Sequence[ArchiveTask],
) -> Sequence[ArchiveTask]:
    async with AsyncSession(engine) as session:
        for task in tasks:
            statement = select(ArchiveTask).where(ArchiveTask.TaskID == task.TaskID)
            if (await session.exec(statement)).first():
                raise exceptions.DataAlreadyExistsError(
                    detail=f"{task.TaskID} already exists"
                )
            session.add(task)

        await session.commit()
        for task in tasks:
            await session.refresh(task)
    return tasks


async def update_archive_tasks_repo(
    tasks: Sequence[ArchiveTask],
) -> Sequence[ArchiveTask]:
    async with AsyncSession(engine) as session:
        for task in tasks:
            statement = select(ArchiveTask).where(ArchiveTask.TaskID == task.TaskID)
            if not (await session.exec(statement)).first():
                raise exceptions.DataNotFoundError(detail=f"{task.TaskID} not found")
            session.add(task)

        await session.commit()
        for task in tasks:
            await session.refresh(task)
    return tasks


async def delete_archive_tasks_repo(task_ids: list[str]) -> list[str]:
    async with AsyncSession(engine) as session:
        _ = await session.exec(
            delete(ArchiveTask).where(cast(Any, ArchiveTask.TaskID).in_(task_ids))
        )
        await session.commit()
    return task_ids
