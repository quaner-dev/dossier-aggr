from typing import Annotated

from fastapi import APIRouter, Depends

from core import constants
from schemas import VehicleArchive, VehicleArchiveList, VehicleArchiveListSchema
from services import VehicleArchiveConfidenceService

router = APIRouter()


@router.post(
    path=constants.VEHICLE_ARCHIVE_CONFIDENCE_URL,
    response_model=VehicleArchiveListSchema,
    description="GA/T 2350.5-2025 A.18 车辆档案核验接口",
)
async def vehicle_archive_confidence_verify(
    data: VehicleArchiveListSchema,
    service: Annotated[
        VehicleArchiveConfidenceService, Depends(VehicleArchiveConfidenceService)
    ],
) -> VehicleArchiveListSchema:
    archives = data.VehicleArchiveListObject.VehicleArchiveObject
    verified_archives = await service.verify_vehicle_archive_confidence(archives=archives)
    return VehicleArchiveListSchema(
        VehicleArchiveListObject=VehicleArchiveList(
            VehicleArchiveObject=[
                VehicleArchive.model_validate(archive, from_attributes=True)
                for archive in verified_archives
            ]
        )
    )
