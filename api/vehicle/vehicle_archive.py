from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BeforeValidator

import constants
from models import (
    ResponseStatus,
    ResponseStatusList,
    ResponseStatusListSchema,
    VehicleArchiveList,
    VehicleArchiveListSchema,
)
from services import VehicleArchiveService
from utils import parse_id_list

router = APIRouter()


@router.get(
    path=constants.VEHICLE_ARCHIVES_QUERY_SYNC_URL,
    description="GA/T 2350.5-2025 A.11 车辆档案查询接口",
)
async def vehicle_archives_query_sync_read(
    service: Annotated[VehicleArchiveService, Depends(VehicleArchiveService)],
) -> VehicleArchiveListSchema:
    archives = await service.list_vehicle_archives()
    return VehicleArchiveListSchema(
        VehicleArchiveListObject=VehicleArchiveList(
            VehicleArchiveObject=[archive for archive in archives]
        )
    )


@router.post(
    path=constants.VEHICLE_ARCHIVES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.12 车辆档案增加接口",
)
async def vehicle_archives_create(
    data: VehicleArchiveListSchema,
    service: Annotated[VehicleArchiveService, Depends(VehicleArchiveService)],
) -> ResponseStatusListSchema:
    archives = data.VehicleArchiveListObject.VehicleArchiveObject
    _ = await service.create_vehicle_archives(archives=archives)
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.VEHICLE_ARCHIVES_URL,
                    StatusCode="0",
                    StatusString="新增成功",
                    Id=archive.ArchiveID,
                    LocalTime=datetime.now(),
                )
                for archive in archives
            ]
        )
    )


@router.put(
    path=constants.VEHICLE_ARCHIVES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.12 车辆档案更新接口",
)
async def vehicle_archives_update(
    data: VehicleArchiveListSchema,
    service: Annotated[VehicleArchiveService, Depends(VehicleArchiveService)],
) -> ResponseStatusListSchema:
    archives = data.VehicleArchiveListObject.VehicleArchiveObject
    _ = await service.update_vehicle_archives(archives=archives)
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.VEHICLE_ARCHIVES_URL,
                    StatusCode="0",
                    StatusString="更新成功",
                    Id=archive.ArchiveID,
                    LocalTime=datetime.now(),
                )
                for archive in archives
            ]
        )
    )


@router.delete(
    path=constants.VEHICLE_ARCHIVES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.12 车辆档案删除接口",
)
async def vehicle_archives_delete(
    archive_ids: Annotated[list[str], BeforeValidator(parse_id_list)],
    service: Annotated[VehicleArchiveService, Depends(VehicleArchiveService)],
):
    _ = await service.delete_vehicle_archives(archive_ids=archive_ids)
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.VEHICLE_ARCHIVES_URL,
                    StatusCode="0",
                    StatusString="删除成功",
                    Id=archive_id,
                    LocalTime=datetime.now(),
                )
                for archive_id in archive_ids
            ]
        )
    )
