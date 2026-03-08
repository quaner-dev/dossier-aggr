from collections.abc import Sequence
from typing import Any, cast

import exceptions
from database import engine
from models.task.archive_task import ArchiveTask
from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession


async def list_archive_tasks_repo() -> Sequence[ArchiveTask]:
    async with AsyncSession(engine) as session:
        tasks = (await session.exec(select(ArchiveTask))).all()
        if not tasks:
            raise exceptions.DataNotFoundError(detail="No ArchiveTask data exist")
        return tasks


async def create_archive_tasks_repo(tasks: list[ArchiveTask]) -> Sequence[ArchiveTask]:
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


async def update_archive_tasks_repo(tasks: list[ArchiveTask]) -> Sequence[ArchiveTask]:
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
        _ = await session.exec(delete(ArchiveTask).where(cast(Any, ArchiveTask.TaskID).in_(task_ids)))
        await session.commit()
    return task_ids
