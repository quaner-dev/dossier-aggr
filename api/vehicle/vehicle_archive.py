from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BeforeValidator

from core import constants
from models import (
    ArchiveQueryResult,
    ArchiveQueryResultSchema,
    ArchiveQuerySchema,
    ResponseStatus,
    ResponseStatusList,
    ResponseStatusListSchema,
    VehicleArchiveList,
    VehicleArchiveListSchema,
)
from services import VehicleArchiveService
from core.utils import parse_id_list

router = APIRouter()


@router.post(
    path=constants.VEHICLE_ARCHIVES_QUERY_SYNC_URL,
    description="GA/T 2350.5-2025 A.11 车辆档案查询接口",
)
async def vehicle_archives_query_sync(
    data: ArchiveQuerySchema,
    service: Annotated[VehicleArchiveService, Depends(VehicleArchiveService)],
) -> ArchiveQueryResultSchema:
    query = data.ArchiveQueryObject
    archives = await service.query_vehicle_archives(query=query)
    record_start_no = query.RecordStartNo or 0
    record_limit = query.PageRecordNum or query.MaxNumRecordReturn or len(archives)
    page_archives = archives[record_start_no : record_start_no + record_limit]
    return ArchiveQueryResultSchema(
        ArchiveQueryResultObject=ArchiveQueryResult(
            QueryID=query.QueryID,
            RecordStartNo=record_start_no,
            PageRecordNum=len(page_archives),
            TotalNum=len(archives),
            VehicleArchiveListObject=VehicleArchiveList(
                VehicleArchiveObject=[archive for archive in page_archives]
            ),
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
    archive_ids: Annotated[
        list[str], BeforeValidator(parse_id_list), Query(alias="IDList")
    ],
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
