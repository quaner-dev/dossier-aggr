from datetime import datetime

from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BeforeValidator

import constants
from models import ResponseStatus, ResponseStatusList, ResponseStatusListSchema
from services import VehicleArchiveConfidenceService
from utils import parse_id_list

router = APIRouter()


@router.post(
    path=constants.VEHICLE_ARCHIVE_CONFIDENCE_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.18 车辆档案核验接口",
)
async def vehicle_archive_confidence_verify(
    archive_ids: Annotated[list[str], BeforeValidator(parse_id_list)],
    service: Annotated[
        VehicleArchiveConfidenceService, Depends(VehicleArchiveConfidenceService)
    ],
) -> ResponseStatusListSchema:
    verified_ids = await service.verify_vehicle_archive_confidence(archive_ids=archive_ids)
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.VEHICLE_ARCHIVE_CONFIDENCE_URL,
                    StatusCode="0",
                    StatusString="核验完成",
                    Id=archive_id,
                    LocalTime=datetime.now(),
                )
                for archive_id in verified_ids
            ]
        )
    )
