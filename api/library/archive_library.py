from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from pydantic import BeforeValidator

from core import constants
from core.time import CHINA_TZ
from core.utils import parse_id_list
from schemas import (
    ArchiveLibraryList,
    ArchiveLibraryListSchema,
    ResponseStatus,
    ResponseStatusList,
    ResponseStatusListSchema,
)
from services import ArchiveLibraryService

router = APIRouter()


@router.get(
    path=constants.ARCHIVE_LIBRARIES_URL,
    description="GA/T 2350.5-2025 A.5 目标档案库查询接口",
)
async def archive_libraries_query(
    request: Request,
    service: Annotated[ArchiveLibraryService, Depends(ArchiveLibraryService)],
) -> ArchiveLibraryListSchema:
    libraries = await service.list_archive_libraries(filters=dict(request.query_params))
    return ArchiveLibraryListSchema(
        ArchiveLibraryListObject=ArchiveLibraryList(
            ArchiveLibraryObject=list(libraries)
        )
    )


@router.post(
    path=constants.ARCHIVE_LIBRARIES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.5 目标档案库增加接口",
)
async def archive_library_create(
    data: ArchiveLibraryListSchema,
    service: Annotated[ArchiveLibraryService, Depends(ArchiveLibraryService)],
) -> ResponseStatusListSchema:
    libraries = data.ArchiveLibraryListObject.ArchiveLibraryObject
    _ = await service.create_archive_libraries(libraries=libraries)
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.ARCHIVE_LIBRARIES_URL,
                    StatusCode="0",
                    StatusString="新增成功",
                    Id=library.ArchiveLibraryID,
                    LocalTime=datetime.now(tz=CHINA_TZ),
                )
                for library in libraries
            ]
        )
    )


@router.put(
    path=constants.ARCHIVE_LIBRARIES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.5 目标档案库更新接口",
)
async def archive_library_update(
    data: ArchiveLibraryListSchema,
    service: Annotated[ArchiveLibraryService, Depends(ArchiveLibraryService)],
) -> ResponseStatusListSchema:
    libraries = data.ArchiveLibraryListObject.ArchiveLibraryObject
    _ = await service.update_archive_libraries(libraries=libraries)
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.ARCHIVE_LIBRARIES_URL,
                    StatusCode="0",
                    StatusString="修改成功",
                    Id=library.ArchiveLibraryID,
                    LocalTime=datetime.now(tz=CHINA_TZ),
                )
                for library in libraries
            ]
        )
    )


@router.delete(
    path=constants.ARCHIVE_LIBRARIES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.5 目标档案库删除接口",
)
async def archive_library_delete(
    library_ids: Annotated[
        list[str], BeforeValidator(parse_id_list), Query(alias="IDList")
    ],
    service: Annotated[ArchiveLibraryService, Depends(ArchiveLibraryService)],
) -> ResponseStatusListSchema:
    _ = await service.delete_archive_libraries(library_ids=library_ids)
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.ARCHIVE_LIBRARIES_URL,
                    StatusCode="0",
                    StatusString="删除成功",
                    Id=library_id,
                    LocalTime=datetime.now(tz=CHINA_TZ),
                )
                for library_id in library_ids
            ]
        )
    )
