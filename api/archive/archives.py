from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BeforeValidator

from core import constants
from core.settings import CHINA_TZ
from core.utils import parse_id_list
from schemas import (
    Archive,
    ArchiveList,
    ArchiveListSchema,
    ArchiveQueryResult,
    ArchiveQueryResultSchema,
    ArchiveQuerySchema,
    ResponseStatus,
    ResponseStatusList,
    ResponseStatusListSchema,
)
from services import ArchiveService

router = APIRouter()


@router.post(
    path=constants.ARCHIVES_QUERY_SYNC_URL,
    description="GA/T 2350.5-2025 A.9 人员档案查询接口",
)
async def archives_query_sync(
    data: ArchiveQuerySchema,
    service: Annotated[ArchiveService, Depends(ArchiveService)],
) -> ArchiveQueryResultSchema:
    """处理 A.9 人员档案同步查询并包装 `ArchiveQueryResultObject`。

    Repo/service 返回完整匹配集合；路由层按协议分页字段裁剪本页结果，
    并生成查询结果顶层包装对象。
    """

    query = data.ArchiveQueryObject
    archives = await service.query_archives(query=query)
    record_start_no = query.RecordStartNo or 0
    record_limit = query.PageRecordNum or query.MaxNumRecordReturn or len(archives)
    page_archives = archives[record_start_no : record_start_no + record_limit]
    return ArchiveQueryResultSchema(
        ArchiveQueryResultObject=ArchiveQueryResult(
            QueryID=query.QueryID,
            RecordStartNo=record_start_no,
            PageRecordNum=len(page_archives),
            TotalNum=len(archives),
            ArchiveListObject=ArchiveList(
                ArchiveObject=[
                    Archive.model_validate(archive, from_attributes=True)
                    for archive in page_archives
                ]
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
    """处理 A.10 人员档案批量新增并返回逐档案状态。"""

    archives = data.ArchiveListObject.ArchiveObject
    _ = await service.create_archives(archives=archives)
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.ARCHIVES_URL,
                    StatusCode="0",
                    StatusString="已接收",
                    Id=archive.ArchiveID,
                    LocalTime=datetime.now(tz=CHINA_TZ),
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
    """处理 A.10 人员档案批量更新并返回逐档案状态。"""

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
                    LocalTime=datetime.now(tz=CHINA_TZ),
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
    archive_ids: Annotated[
        list[str], BeforeValidator(parse_id_list), Query(alias="IDList")
    ],
    service: Annotated[ArchiveService, Depends(ArchiveService)],
) -> ResponseStatusListSchema:
    """处理 A.10 人员档案批量删除。

    `IDList` 在参数边界解析为档案标识列表，响应按传入 ID 生成
    `ResponseStatusListObject`。
    """

    _ = await service.delete_archives(archive_ids=archive_ids)
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.ARCHIVES_URL,
                    StatusCode="0",
                    StatusString="删除成功",
                    Id=archive_id,
                    LocalTime=datetime.now(tz=CHINA_TZ),
                )
                for archive_id in archive_ids
            ]
        )
    )
