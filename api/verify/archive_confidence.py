from datetime import datetime

from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BeforeValidator

from core import constants
from models import ResponseStatus, ResponseStatusList, ResponseStatusListSchema
from services import ArchiveConfidenceService
from core.utils import parse_id_list

router = APIRouter()


@router.post(
    path=constants.ARCHIVE_CONFIDENCE_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.17 人员档案核验接口",
)
async def archive_confidence_verify(
    archive_ids: Annotated[list[str], BeforeValidator(parse_id_list)],
    service: Annotated[ArchiveConfidenceService, Depends(ArchiveConfidenceService)],
) -> ResponseStatusListSchema:
    verified_ids = await service.verify_archive_confidence(archive_ids=archive_ids)
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.ARCHIVE_CONFIDENCE_URL,
                    StatusCode="0",
                    StatusString="核验完成",
                    Id=archive_id,
                    LocalTime=datetime.now(),
                )
                for archive_id in verified_ids
            ]
        )
    )
