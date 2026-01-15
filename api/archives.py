from datetime import datetime

from fastapi import APIRouter, Depends, Query

import constants
from schemas import (
    ArchiveQueryResultSchema,
    ArchiveQuerySchema,
    ResponseStatusListSchema,
    ResponseStatus,
    ResponseStatusList,
    ArchiveListSchema,
)
from services import ArchiveService

router = APIRouter()


@router.get(
    path=constants.ARCHIVES_QUERY_SYNC_URL,
    response_model=ArchiveQueryResultSchema,
    description="GA/T 2350.5-2025 A.9 人员档案查询接口",
)
async def archives_query_sync_read(
    data: ArchiveQuerySchema,
    service: ArchiveService = Depends(ArchiveService),
):
    archive_query = data.ArchiveQueryObject
    archives = await service.list_archives(archive_query)
    return archives


@router.post(
    path=constants.ARCHIVES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.10 人员档案增加接口",
)
async def archives_create(data: ArchiveListSchema):
    archives = data.ArchiveListObject.ArchiveObject

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.ARCHIVES_URL,
            StatusCode="0",
            StatusString="档案创建成功",
            Id=archive.ArchiveID,
            LocalTime=datetime.now(),
        )
        for archive in archives
    ]
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )


@router.put(
    path=constants.ARCHIVES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.10 人员档案更新接口",
)
async def archives_update(data: ArchiveListSchema):
    archives = data.ArchiveListObject.ArchiveObject

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.ARCHIVES_URL,
            StatusCode="0",
            StatusString="档案更新成功",
            Id=archive.ArchiveID,
            LocalTime=datetime.now(),
        )
        for archive in archives
    ]
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )


@router.delete(
    path=constants.ARCHIVES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.10 人员档案删除接口",
)
async def archives_delete(
    id_list: str = Query(..., alias="IDList"),
    service: ArchiveService = Depends(ArchiveService),
):
    """批量档案删除接口"""
    archive_ids = [id.strip() for id in id_list.split(",")]
    
    for archive_id in archive_ids:
        await service.delete_archive(archive_id)

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.ARCHIVES_URL,
            StatusCode="0",
            StatusString="删除成功",
            Id=archive_id,
            LocalTime=datetime.now(),
        )
        for archive_id in archive_ids
    ]

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )
