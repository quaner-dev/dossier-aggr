from collections.abc import Sequence

from domain import ArchiveSubject as ArchiveSubjectData
from models import ArchiveSubject
from repo.archive.archive_subject import (
    create_archive_subjects_repo,
    delete_archive_subjects_repo,
    query_archive_subjects_repo,
    update_archive_subjects_repo,
)
from schemas import ArchiveSubjectQuery
from services.model_conversion import to_table_models


class ArchiveSubjectService:
    """编排 GA/T 2350.5 A.13/A.14 人员档案明细业务链路。

    查询、创建、更新和多键删除统一委托 repo。
    """

    async def query_archive_subjects(
        self, query: ArchiveSubjectQuery | None = None
    ) -> list[ArchiveSubject]:
        return list(await query_archive_subjects_repo(query=query))

    async def create_archive_subjects(
        self, subjects: Sequence[ArchiveSubjectData]
    ) -> list[ArchiveSubject]:
        return list(await create_archive_subjects_repo(subjects=to_table_models(ArchiveSubject, subjects)))

    async def update_archive_subjects(
        self, subjects: Sequence[ArchiveSubjectData]
    ) -> list[ArchiveSubject]:
        return list(await update_archive_subjects_repo(subjects=to_table_models(ArchiveSubject, subjects)))

    async def delete_archive_subjects(
        self,
        archive_id: str | None = None,
        face_id_list: list[str] | None = None,
        person_id_list: list[str] | None = None,
        motor_vehicle_id_list: list[str] | None = None,
        non_motor_vehicle_id_list: list[str] | None = None,
    ) -> list[str]:
        return await delete_archive_subjects_repo(
            archive_id=archive_id,
            face_id_list=face_id_list,
            person_id_list=person_id_list,
            motor_vehicle_id_list=motor_vehicle_id_list,
            non_motor_vehicle_id_list=non_motor_vehicle_id_list,
        )
