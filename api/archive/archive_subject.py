from fastapi import APIRouter, Depends

import constants
from models import ArchiveSubjectSchema, ResponseStatusListSchema
from services import ArchiveSubjectService

router = APIRouter()


@router.post(
    path=constants.ARCHIVE_SUBJECT_QUERY_SYNC_URL,
    description="GA/T 2350.5-2025 A.13 人员档案明细查询接口",
)
async def archive_subject_query_sync_read(): ...


@router.post(
    path=constants.ARCHIVE_SUBJECTS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.14 人员档案明细增加接口",
)
async def archive_subjects_create(
    data: ArchiveSubjectSchema,
    service: ArchiveSubjectService = Depends(ArchiveSubjectService),
): ...


@router.put(
    path=constants.ARCHIVE_SUBJECTS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.14 人员档案明细更新接口",
)
async def archive_subjects_update(
    data: ArchiveSubjectSchema,
    service: ArchiveSubjectService = Depends(ArchiveSubjectService),
): ...


@router.delete(
    path=constants.ARCHIVE_SUBJECTS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.14 人员档案明细删除接口",
)
async def archive_subjects_delete(
    archive_id: str | None = None,
    face_id_list: str | None = None,
    person_id_list: str | None = None,
    motor_vehicle_id_list: str | None = None,
    non_motor_vehicle_id_list: str | None = None,
    service: ArchiveSubjectService = Depends(ArchiveSubjectService),
): ...
