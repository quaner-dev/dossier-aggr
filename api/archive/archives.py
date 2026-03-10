from fastapi import APIRouter
from datetime import datetime
from typing import Annotated
from pydantic import BeforeValidator

from core import constants
from models import (
    ArchiveList,
    ArchiveListSchema,
    ArchiveQueryResult,
    ArchiveQueryResultSchema,
    ResponseStatusList,
    ResponseStatus,
    ResponseStatusListSchema,
)
from services import ArchiveService
from fastapi import Depends
from core.utils import parse_id_list

router = APIRouter()


@router.get(
    path=constants.ARCHIVES_QUERY_SYNC_URL,
    description="GA/T 2350.5-2025 A.9 人员档案查询接口",
)
async def archives_query_sync(
    service: Annotated[ArchiveService, Depends(ArchiveService)],
) -> ArchiveQueryResultSchema:
    archives = await service.list_archives()
    return ArchiveQueryResultSchema(
        ArchiveQueryResultObject=ArchiveQueryResult(
            QueryID="LOCAL_QUERY",
            RecordStartNo=0,
            PageRecordNum=len(archives),
            TotalNum=len(archives),
            ArchiveListObject=ArchiveList(
                ArchiveObject=[archive for archive in archives]
            ),
        )
    )


@router.post(
    path=constants.ARCHIVES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.10 人员档案增加接口",
)
async def archives_create(
    data: ArchiveListSchema,
    service: Annotated[ArchiveService, Depends(ArchiveService)],
) -> ResponseStatusListSchema:
    archives = data.ArchiveListObject.ArchiveObject
    _ = await service.create_archives(archives=archives)
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.ARCHIVES_URL,
                    StatusCode="0",
                    StatusString="新增成功",
                    Id=archive.ArchiveID,
                    LocalTime=datetime.now(),
                )
                for archive in archives
            ]
        )
    )


@router.put(
    path=constants.ARCHIVES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.10 人员档案更新接口",
)
async def archives_update(
    data: ArchiveListSchema,
    service: Annotated[ArchiveService, Depends(ArchiveService)],
) -> ResponseStatusListSchema:
    archives = data.ArchiveListObject.ArchiveObject
    _ = await service.update_archives(archives=archives)
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.ARCHIVES_URL,
                    StatusCode="0",
                    StatusString="修改成功",
                    Id=archive.ArchiveID,
                    LocalTime=datetime.now(),
                )
                for archive in archives
            ]
        )
    )


@router.delete(
    path=constants.ARCHIVES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.10 人员档案删除接口",
)
async def archives_delete(
    archive_ids: Annotated[list[str], BeforeValidator(parse_id_list)],
    service: Annotated[ArchiveService, Depends(ArchiveService)],
) -> ResponseStatusListSchema:
    _ = await service.delete_archives(archive_ids=archive_ids)
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.ARCHIVES_URL,
                    StatusCode="0",
                    StatusString="删除成功",
                    Id=archive_id,
                    LocalTime=datetime.now(),
                )
                for archive_id in archive_ids
            ]
        )
    )
