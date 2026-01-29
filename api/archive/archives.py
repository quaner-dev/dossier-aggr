from fastapi import APIRouter

import constants
from models import (
    ResponseStatusListSchema,
)

router = APIRouter()


@router.get(
    path=constants.ARCHIVES_QUERY_SYNC_URL,
    description="GA/T 2350.5-2025 A.9 人员档案查询接口",
)
async def archives_query_sync_read(): ...


@router.post(
    path=constants.ARCHIVES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.10 人员档案增加接口",
)
async def archives_create(): ...


@router.put(
    path=constants.ARCHIVES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.10 人员档案更新接口",
)
async def archives_update(): ...


@router.delete(
    path=constants.ARCHIVES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.10 人员档案删除接口",
)
async def archives_delete(): ...
