from fastapi import APIRouter, Depends
from datetime import datetime
from typing import Annotated

import constants
from models import (
    ArchiveSubjectSchema,
    ArchiveSubjectList,
    ArchiveSubjectQueryResult,
    ArchiveSubjectQueryResultSchema,
    ArchiveList,
    ResponseStatusListSchema,
    ResponseStatusList,
    ResponseStatus,
)
from services import ArchiveSubjectService
from utils import parse_id_list

router = APIRouter()


@router.post(
    path=constants.ARCHIVE_SUBJECT_QUERY_SYNC_URL,
    description="GA/T 2350.5-2025 A.13 人员档案明细查询接口",
)
async def archive_subject_query_sync_read(
    service: Annotated[ArchiveSubjectService, Depends(ArchiveSubjectService)],
) -> ArchiveSubjectQueryResultSchema:
    subjects = await service.query_archive_subjects()
    return ArchiveSubjectQueryResultSchema(
        ArchiveSubjectQueryResultObject=ArchiveSubjectQueryResult(
            QueryID="LOCAL_QUERY",
            RecordStartNo=0,
            PageRecordNum=len(subjects),
            TotalNum=len(subjects),
            ArchiveListObject=ArchiveList(ArchiveObject=[]),
            ArchiveSubjectInfoList=ArchiveSubjectList(ArchiveSubjectObject=subjects),
        )
    )


@router.post(
    path=constants.ARCHIVE_SUBJECTS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.14 人员档案明细增加接口",
)
async def archive_subjects_create(
    data: ArchiveSubjectSchema,
    service: ArchiveSubjectService = Depends(ArchiveSubjectService),
) -> ResponseStatusListSchema:
    subjects = data.ArchiveSubjectListObject.ArchiveSubjectObject
    _ = await service.create_archive_subjects(subjects=subjects)
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.ARCHIVE_SUBJECTS_URL,
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
    path=constants.ARCHIVE_SUBJECTS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.14 人员档案明细更新接口",
)
async def archive_subjects_update(
    data: ArchiveSubjectSchema,
    service: ArchiveSubjectService = Depends(ArchiveSubjectService),
) -> ResponseStatusListSchema:
    subjects = data.ArchiveSubjectListObject.ArchiveSubjectObject
    _ = await service.update_archive_subjects(subjects=subjects)
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.ARCHIVE_SUBJECTS_URL,
                    StatusCode="0",
                    StatusString="修改成功",
                    Id=subject.ArchiveID,
                    LocalTime=datetime.now(),
                )
                for subject in subjects
            ]
        )
    )


@router.delete(
    path=constants.ARCHIVE_SUBJECTS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.14 人员档案明细删除接口",
)
async def archive_subjects_delete(
    archive_id: str | None = None,
    face_id_list: str | list[str] | None = None,
    person_id_list: str | list[str] | None = None,
    motor_vehicle_id_list: str | list[str] | None = None,
    non_motor_vehicle_id_list: str | list[str] | None = None,
    service: ArchiveSubjectService = Depends(ArchiveSubjectService),
) -> ResponseStatusListSchema:
    parsed_face_ids = parse_id_list(face_id_list) if face_id_list else None
    parsed_person_ids = parse_id_list(person_id_list) if person_id_list else None
    parsed_motor_vehicle_ids = (
        parse_id_list(motor_vehicle_id_list) if motor_vehicle_id_list else None
    )
    parsed_non_motor_vehicle_ids = (
        parse_id_list(non_motor_vehicle_id_list) if non_motor_vehicle_id_list else None
    )

    deleted_ids = await service.delete_archive_subjects(
        archive_id=archive_id,
        face_id_list=parsed_face_ids,
        person_id_list=parsed_person_ids,
        motor_vehicle_id_list=parsed_motor_vehicle_ids,
        non_motor_vehicle_id_list=parsed_non_motor_vehicle_ids,
    )

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.ARCHIVE_SUBJECTS_URL,
                    StatusCode="0",
                    StatusString="删除成功",
                    Id=deleted_id,
                    LocalTime=datetime.now(),
                )
                for deleted_id in deleted_ids
            ]
        )
    )
