from datetime import datetime

from fastapi import APIRouter, Depends

import constants
from models import (
    ArchiveLibraryList,
    ResponseStatusListSchema,
    ResponseStatus,
    ResponseStatusList,
)
from services import ArchiveLibraryService

router = APIRouter()


@router.get(
    path=constants.ARCHIVE_LIBRARY_QUERY_SYNC_URL,
    description="GA/T 2350.5-2025 A.5 档案库查询接口",
)
async def archive_library_query_sync_read(
    service: ArchiveLibraryService = Depends(ArchiveLibraryService),
): ...


@router.post(
    path=constants.ARCHIVE_LIBRARY_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.6 档案库增加接口",
)
async def archive_library_create(
    service: ArchiveLibraryService = Depends(ArchiveLibraryService),
): ...


@router.put(
    path=constants.ARCHIVE_LIBRARY_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.7 档案库更新接口",
)
async def archive_library_update(
    service: ArchiveLibraryService = Depends(ArchiveLibraryService),
): ...


@router.delete(
    path=constants.ARCHIVE_LIBRARY_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.8 档案库删除接口",
)
async def archive_library_delete(
    id_list: str,
    service: ArchiveLibraryService = Depends(ArchiveLibraryService),
): ...
