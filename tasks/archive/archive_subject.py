from collections.abc import Sequence

import brokers
from models import ArchiveSubject
from repo.archive.archive_subject import (
    create_archive_subjects_repo,
    delete_archive_subjects_repo,
    query_archive_subjects_repo,
    update_archive_subjects_repo,
)


async def query_archive_subjects_task() -> Sequence[ArchiveSubject]:
    return await query_archive_subjects_repo()


@brokers.broker.task
async def create_archive_subjects_task(
    subjects: list[ArchiveSubject],
) -> Sequence[ArchiveSubject]:
    return await create_archive_subjects_repo(subjects=subjects)


@brokers.broker.task
async def update_archive_subjects_task(
    subjects: list[ArchiveSubject],
) -> Sequence[ArchiveSubject]:
    return await update_archive_subjects_repo(subjects=subjects)


@brokers.broker.task
async def delete_archive_subjects_task(archive_id: str) -> list[str]:
    return await delete_archive_subjects_repo(archive_id=archive_id)
