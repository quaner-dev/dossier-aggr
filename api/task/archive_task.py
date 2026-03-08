from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BeforeValidator
from typing import Annotated

import constants
from models import (
    ResponseStatusListSchema,
    ResponseStatusList,
    ResponseStatus,
    ArchiveTaskList,
    ArchiveTaskListSchema,
)
from services import ArchiveTaskService
from utils import parse_id_list

router = APIRouter()


@router.get(
    path=constants.ARCHIVE_TASKS_URL,
    description="GA/T 2350.5-2025 A.6 聚档任务查询接口",
)
async def archive_tasks_query(
    service: Annotated[ArchiveTaskService, Depends(ArchiveTaskService)],
) -> ArchiveTaskListSchema:
    tasks = await service.list_archive_tasks()
    return ArchiveTaskListSchema(
        ArchiveTaskListObject=ArchiveTaskList(ArchiveTaskObject=[task for task in tasks])
    )


@router.post(
    path=constants.ARCHIVE_TASKS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.6 聚档任务增加接口",
)
async def archive_tasks_create(
    data: ArchiveTaskListSchema,
    service: Annotated[ArchiveTaskService, Depends(ArchiveTaskService)],
) -> ResponseStatusListSchema:
    tasks = data.ArchiveTaskListObject.ArchiveTaskObject
    _ = await service.create_archive_tasks(tasks=tasks)
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.ARCHIVE_TASKS_URL,
                    StatusCode="0",
                    StatusString="新增成功",
                    Id=task.TaskID,
                    LocalTime=datetime.now(),
                )
                for task in tasks
            ]
        )
    )


@router.put(
    path=constants.ARCHIVE_TASKS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.6 聚档任务更新接口",
)
async def archive_tasks_update(
    data: ArchiveTaskListSchema,
    service: Annotated[ArchiveTaskService, Depends(ArchiveTaskService)],
) -> ResponseStatusListSchema:
    tasks = data.ArchiveTaskListObject.ArchiveTaskObject
    _ = await service.update_archive_tasks(tasks=tasks)
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.ARCHIVE_TASKS_URL,
                    StatusCode="0",
                    StatusString="更新成功",
                    Id=task.TaskID,
                    LocalTime=datetime.now(),
                )
                for task in tasks
            ]
        )
    )


@router.delete(
    path=constants.ARCHIVE_TASKS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.6 聚档任务删除接口",
)
async def archive_tasks_delete(
    task_ids: Annotated[list[str], BeforeValidator(parse_id_list)],
    service: Annotated[ArchiveTaskService, Depends(ArchiveTaskService)],
):
    _ = await service.delete_archive_tasks(task_ids=task_ids)
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.ARCHIVE_TASKS_URL,
                    StatusCode="0",
                    StatusString="删除成功",
                    Id=task_id,
                    LocalTime=datetime.now(),
                )
                for task_id in task_ids
            ]
        )
    )
