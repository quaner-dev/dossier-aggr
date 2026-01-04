from fastapi import APIRouter

from schemas.archive_subject_query import ArchiveSubjectQuerySchema
import constants

router = APIRouter()


@router.post(
    path=constants.ARCHIVE_SUBJECT_QUERY_SYNC_URL,
    response_model="",
    description="GA/T 2350.5-2025 A.13 人员档案明细查询接口",
)
async def archive_subject_query_sync_read(data: ArchiveSubjectQuerySchema): ...
