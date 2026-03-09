from models import ArchiveSubject
from repositories.archive.archive_subject import query_archive_subjects_repo
from tasks.archive.archive_subject import (
    create_archive_subjects_task,
    update_archive_subjects_task,
    delete_archive_subjects_task,
)
from services.task_dispatch import dispatch_and_wait


class ArchiveSubjectService:
    async def query_archive_subjects(self) -> list[ArchiveSubject]:
        return list(await query_archive_subjects_repo())

    async def create_archive_subjects(
        self, subjects: list[ArchiveSubject]
    ) -> list[ArchiveSubject]:
        return await dispatch_and_wait(create_archive_subjects_task, subjects=subjects)

    async def update_archive_subjects(
        self, subjects: list[ArchiveSubject]
    ) -> list[ArchiveSubject]:
        return await dispatch_and_wait(update_archive_subjects_task, subjects=subjects)

    async def delete_archive_subjects(
        self, archive_id: str
    ) -> list[str]:
        return await dispatch_and_wait(delete_archive_subjects_task, archive_id=archive_id)
