from typing import Annotated

from fastapi import APIRouter, Depends

from core import constants
from models import ArchiveList, ArchiveListSchema
from services import ArchiveConfidenceService

router = APIRouter()


@router.post(
    path=constants.ARCHIVE_CONFIDENCE_URL,
    response_model=ArchiveListSchema,
    description="GA/T 2350.5-2025 A.17 人员档案核验接口",
)
async def archive_confidence_verify(
    data: ArchiveListSchema,
    service: Annotated[ArchiveConfidenceService, Depends(ArchiveConfidenceService)],
) -> ArchiveListSchema:
    archives = data.ArchiveListObject.ArchiveObject
    verified_archives = await service.verify_archive_confidence(archives=archives)
    return ArchiveListSchema(
        ArchiveListObject=ArchiveList(ArchiveObject=verified_archives)
    )
