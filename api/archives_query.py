from fastapi import Depends, APIRouter


from schemas import ArchiveQuerySchema, ArchiveQueryResultSchema
import constants
from services.archives_query import ArchivesQueryService

router = APIRouter()


@router.get(
    path=constants.ARCHIVES_QUERY_SYNC_URL,
    response_model=ArchiveQueryResultSchema,
    description="GA/T 2350.5-2025 A.9 人员档案查询接口",
)
async def archives_query_sync_read(
    data: ArchiveQuerySchema,
    service: ArchivesQueryService = Depends(ArchivesQueryService),
):
    archive_query = data.ArchiveQueryObject
    archives = await service.list_archives(archive_query)
    return archives
