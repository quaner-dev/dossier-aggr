from models import ArchiveSubject, ArchiveSubjectQuery
from repo.archive.archive_subject import query_archive_subjects_repo
from tasks.archive.archive_subject import (
    create_archive_subjects_task,
    update_archive_subjects_task,
    delete_archive_subjects_task,
)
from services.task_dispatch import dispatch_and_wait


class ArchiveSubjectService:
    """编排 GA/T 2350.5 A.13/A.14 人员档案明细业务链路。

    查询由 repo 解释 `ArchiveSubjectQuery`；写入和多删除键删除均通过
    Taskiq task 进入持久化层，避免 service 直接处理数据库细节。
    """

    async def query_archive_subjects(
        self, query: ArchiveSubjectQuery | None = None
    ) -> list[ArchiveSubject]:
        return list(await query_archive_subjects_repo(query=query))

    async def create_archive_subjects(
        self, subjects: list[ArchiveSubject]
    ) -> list[ArchiveSubject]:
        return list(await dispatch_and_wait(create_archive_subjects_task, subjects=subjects))

    async def update_archive_subjects(
        self, subjects: list[ArchiveSubject]
    ) -> list[ArchiveSubject]:
        return list(await dispatch_and_wait(update_archive_subjects_task, subjects=subjects))

    async def delete_archive_subjects(
        self,
        archive_id: str | None = None,
        face_id_list: list[str] | None = None,
        person_id_list: list[str] | None = None,
        motor_vehicle_id_list: list[str] | None = None,
        non_motor_vehicle_id_list: list[str] | None = None,
    ) -> list[str]:
        return await dispatch_and_wait(
            delete_archive_subjects_task,
            archive_id=archive_id,
            face_id_list=face_id_list,
            person_id_list=person_id_list,
            motor_vehicle_id_list=motor_vehicle_id_list,
            non_motor_vehicle_id_list=non_motor_vehicle_id_list,
        )
