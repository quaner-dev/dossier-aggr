from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from core import constants
from models import (
    ArchiveList,
    ArchiveSubjectQueryResult,
    ArchiveSubjectQueryResultSchema,
    ArchiveSubjectQuerySchema,
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
    data: ArchiveSubjectQuerySchema,
    service: Annotated[
        VehicleArchiveSubjectService, Depends(VehicleArchiveSubjectService)
    ],
) -> ArchiveSubjectQueryResultSchema:
    query = data.ArchiveSubjectQueryObject
    subjects = await service.query_vehicle_archive_subjects(query=query)
    record_start_no = query.RecordStartNo or 0
    record_limit = query.PageRecordNum or query.MaxNumRecordReturn or len(subjects)
    page_subjects = subjects[record_start_no : record_start_no + record_limit]
    return ArchiveSubjectQueryResultSchema(
        ArchiveSubjectQueryResultObject=ArchiveSubjectQueryResult(
            QueryID=query.QueryID,
            RecordStartNo=record_start_no,
            PageRecordNum=len(page_subjects),
            TotalNum=len(subjects),
            ArchiveListObject=ArchiveList(ArchiveObject=[]),
            ArchiveSubjectInfoList=VehicleArchiveSubjectList(
                VehicleArchiveSubjectObject=[subject for subject in page_subjects]
            ),
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
    archive_id: Annotated[str | None, Query(alias="ArchiveID")] = None,
    face_id_list: Annotated[str | None, Query(alias="FaceIDList")] = None,
    person_id_list: Annotated[str | None, Query(alias="PersonIDList")] = None,
    motor_vehicle_id_list: Annotated[str | None, Query(alias="MotorVehicleIDList")] = None,
    non_motor_vehicle_id_list: Annotated[
        str | None, Query(alias="NonMotorVehicleIDList")
    ] = None,
    service: VehicleArchiveSubjectService = Depends(VehicleArchiveSubjectService),
):
    deleted_ids = await service.delete_vehicle_archive_subjects(
        archive_id=archive_id,
        face_id_list=parse_id_list(face_id_list) if face_id_list else None,
        person_id_list=parse_id_list(person_id_list) if person_id_list else None,
        motor_vehicle_id_list=(
            parse_id_list(motor_vehicle_id_list) if motor_vehicle_id_list else None
        ),
        non_motor_vehicle_id_list=(
            parse_id_list(non_motor_vehicle_id_list)
            if non_motor_vehicle_id_list
            else None
        ),
    )
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
