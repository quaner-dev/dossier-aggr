from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from core import constants
from core.settings import CHINA_TZ
from core.utils import parse_id_list
from schemas import (
    ArchiveList,
    ArchiveSubject,
    ArchiveSubjectList,
    ArchiveSubjectQueryResult,
    ArchiveSubjectQueryResultSchema,
    ArchiveSubjectQuerySchema,
    ArchiveSubjectSchema,
    ResponseStatus,
    ResponseStatusList,
    ResponseStatusListSchema,
)
from services import ArchiveSubjectService

router = APIRouter()


@router.post(
    path=constants.ARCHIVE_SUBJECT_QUERY_SYNC_URL,
    description="GA/T 2350.5-2025 A.13 人员档案明细查询接口",
)
async def archive_subject_query_sync(
    data: ArchiveSubjectQuerySchema,
    service: Annotated[ArchiveSubjectService, Depends(ArchiveSubjectService)],
) -> ArchiveSubjectQueryResultSchema:
    """处理 A.13 人员档案明细同步查询并包装查询结果。

    明细筛选由 service/repo 完成；路由层只负责协议分页字段和
    `ArchiveSubjectQueryResultObject` 顶层包装。
    """

    query = data.ArchiveSubjectQueryObject
    subjects = await service.query_archive_subjects(query=query)
    record_start_no = query.RecordStartNo or 0
    record_limit = query.PageRecordNum or query.MaxNumRecordReturn or len(subjects)
    page_subjects = subjects[record_start_no : record_start_no + record_limit]
    response_subjects = [
        ArchiveSubject.model_validate(subject, from_attributes=True)
        for subject in page_subjects
    ]
    return ArchiveSubjectQueryResultSchema(
        ArchiveSubjectQueryResultObject=ArchiveSubjectQueryResult(
            QueryID=query.QueryID,
            RecordStartNo=record_start_no,
            PageRecordNum=len(page_subjects),
            TotalNum=len(subjects),
            ArchiveListObject=ArchiveList(ArchiveObject=[]),
            ArchiveSubjectInfoList=ArchiveSubjectList(
                ArchiveSubjectObject=response_subjects
            ),
        )
    )


@router.post(
    path=constants.ARCHIVE_SUBJECTS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.14 人员档案明细增加接口",
)
async def archive_subjects_create(
    data: ArchiveSubjectSchema,
    service: Annotated[ArchiveSubjectService, Depends(ArchiveSubjectService)],
) -> ResponseStatusListSchema:
    """处理 A.14 人员档案明细批量新增并返回逐明细状态。"""

    subjects = data.ArchiveSubjectListObject.ArchiveSubjectObject
    _ = await service.create_archive_subjects(subjects=subjects)
    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.ARCHIVE_SUBJECTS_URL,
                    StatusCode="0",
                    StatusString="已接收",
                    Id=subject.ArchiveID,
                    LocalTime=datetime.now(tz=CHINA_TZ),
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
    service: Annotated[ArchiveSubjectService, Depends(ArchiveSubjectService)],
) -> ResponseStatusListSchema:
    """处理 A.14 人员档案明细批量更新并返回逐明细状态。"""

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
                    LocalTime=datetime.now(tz=CHINA_TZ),
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
    service: Annotated[ArchiveSubjectService, Depends(ArchiveSubjectService)],
    archive_id: Annotated[str | None, Query(alias="ArchiveID")] = None,
    face_id_list: Annotated[str | None, Query(alias="FaceIDList")] = None,
    person_id_list: Annotated[str | None, Query(alias="PersonIDList")] = None,
    motor_vehicle_id_list: Annotated[
        str | None, Query(alias="MotorVehicleIDList")
    ] = None,
    non_motor_vehicle_id_list: Annotated[
        str | None, Query(alias="NonMotorVehicleIDList")
    ] = None,
) -> ResponseStatusListSchema:
    """处理 A.14 人员档案明细删除。

    删除条件支持协议定义的 `ArchiveID` 与四类对象 ID 列表；路由层只做
    查询参数解析，实际匹配和删除语义交给 service/repo。
    """

    deleted_ids = await service.delete_archive_subjects(
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
                    RequestURL=constants.ARCHIVE_SUBJECTS_URL,
                    StatusCode="0",
                    StatusString="删除成功",
                    Id=deleted_id,
                    LocalTime=datetime.now(tz=CHINA_TZ),
                )
                for deleted_id in deleted_ids
            ]
        )
    )
