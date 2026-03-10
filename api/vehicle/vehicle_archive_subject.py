from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BeforeValidator

from core import constants
from models import (
    ResponseStatus,
    ResponseStatusList,
    ResponseStatusListSchema,
    VehicleArchiveSubjectList,
    VehicleArchiveSubjectSchema,
)
from services import VehicleArchiveSubjectService
from core.utils import parse_id_list

router = APIRouter()


@router.post(
    path=constants.VEHICLE_ARCHIVE_SUBJECT_QUERY_SYNC_URL,
    description="GA/T 2350.5-2025 A.15 车辆档案明细查询接口",
)
async def vehicle_archive_subject_query_sync_read(
    service: Annotated[
        VehicleArchiveSubjectService, Depends(VehicleArchiveSubjectService)
    ],
) -> VehicleArchiveSubjectSchema:
    subjects = await service.query_vehicle_archive_subjects()
    return VehicleArchiveSubjectSchema(
        VehicleArchiveSubjectListObject=VehicleArchiveSubjectList(
            VehicleArchiveSubjectObject=[subject for subject in subjects]
        )
    )


@router.post(
    path=constants.VEHICLE_ARCHIVE_SUBJECTS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.16 车辆档案明细增加接口",
)
async def vehicle_archive_subjects_create(
    data: VehicleArchiveSubjectSchema,
    service: Annotated[
        VehicleArchiveSubjectService, Depends(VehicleArchiveSubjectService)
    ],
) -> ResponseStatusListSchema:
    subjects = data.VehicleArchiveSubjectListObject.VehicleArchiveSubjectObject
    _ = await service.create_vehicle_archive_subjects(subjects=subjects)
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.VEHICLE_ARCHIVE_SUBJECTS_URL,
                    StatusCode="0",
                    StatusString="新增成功",
                    Id=subject.ArchiveID,
                    LocalTime=datetime.now(),
                )
                for subject in subjects
            ]
        )
    )


@router.put(
    path=constants.VEHICLE_ARCHIVE_SUBJECTS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.16 车辆档案明细更新接口",
)
async def vehicle_archive_subjects_update(
    data: VehicleArchiveSubjectSchema,
    service: Annotated[
        VehicleArchiveSubjectService, Depends(VehicleArchiveSubjectService)
    ],
) -> ResponseStatusListSchema:
    subjects = data.VehicleArchiveSubjectListObject.VehicleArchiveSubjectObject
    _ = await service.update_vehicle_archive_subjects(subjects=subjects)
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.VEHICLE_ARCHIVE_SUBJECTS_URL,
                    StatusCode="0",
                    StatusString="更新成功",
                    Id=subject.ArchiveID,
                    LocalTime=datetime.now(),
                )
                for subject in subjects
            ]
        )
    )


@router.delete(
    path=constants.VEHICLE_ARCHIVE_SUBJECTS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.16 车辆档案明细删除接口",
)
async def vehicle_archive_subjects_delete(
    archive_ids: Annotated[list[str], BeforeValidator(parse_id_list)],
    service: Annotated[
        VehicleArchiveSubjectService, Depends(VehicleArchiveSubjectService)
    ],
):
    deleted_ids = await service.delete_vehicle_archive_subjects(archive_ids=archive_ids)
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.VEHICLE_ARCHIVE_SUBJECTS_URL,
                    StatusCode="0",
                    StatusString="删除成功",
                    Id=deleted_id,
                    LocalTime=datetime.now(),
                )
                for deleted_id in deleted_ids
            ]
        )
    )
