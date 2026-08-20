from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from pydantic import BeforeValidator

from core import constants
from core.time import CHINA_TZ
from core.utils import parse_id_list
from models import (
    ArchiveTaskList,
    ArchiveTaskListSchema,
    ResponseStatus,
    ResponseStatusList,
    ResponseStatusListSchema,
)
from services import ArchiveTaskService

router = APIRouter()


@router.get(
    path=constants.ARCHIVE_TASKS_URL,
    description="GA/T 2350.5-2025 A.6 聚档任务查询接口",
)
async def archive_tasks_query(
    request: Request,
    service: Annotated[ArchiveTaskService, Depends(ArchiveTaskService)],
) -> ArchiveTaskListSchema:
    tasks = await service.list_archive_tasks(filters=dict(request.query_params))
    return ArchiveTaskListSchema(
        ArchiveTaskListObject=ArchiveTaskList(ArchiveTaskObject=list(tasks))
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
    return _archive_task_status_list(tasks, "新增成功")


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
    return _archive_task_status_list(tasks, "修改成功")


@router.delete(
    path=constants.ARCHIVE_TASKS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.6 聚档任务删除接口",
)
async def archive_tasks_delete(
    task_ids: Annotated[
        list[str], BeforeValidator(parse_id_list), Query(alias="IDList")
    ],
    service: Annotated[ArchiveTaskService, Depends(ArchiveTaskService)],
) -> ResponseStatusListSchema:
    _ = await service.delete_archive_tasks(task_ids=task_ids)
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.ARCHIVE_TASKS_URL,
                    StatusCode="0",
                    StatusString="删除成功",
                    Id=task_id,
                    LocalTime=datetime.now(tz=CHINA_TZ),
                )
                for task_id in task_ids
            ]
        )
    )


def _archive_task_status_list(tasks, status_string: str) -> ResponseStatusListSchema:
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.ARCHIVE_TASKS_URL,
                    StatusCode="0",
                    StatusString=status_string,
                    Id=task.TaskID,
                    LocalTime=datetime.now(tz=CHINA_TZ),
                )
                for task in tasks
            ]
        )
    )
