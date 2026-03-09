from collections.abc import Sequence

import brokers
from models import VehicleArchiveSubject
from repo.vehicle.vehicle_archive_subject import (
    create_vehicle_archive_subjects_repo,
    delete_vehicle_archive_subjects_repo,
    query_vehicle_archive_subjects_repo,
    update_vehicle_archive_subjects_repo,
)


async def query_vehicle_archive_subjects_task() -> Sequence[VehicleArchiveSubject]:
    return await query_vehicle_archive_subjects_repo()


@brokers.broker.task
async def create_vehicle_archive_subjects_task(
    subjects: list[VehicleArchiveSubject],
) -> Sequence[VehicleArchiveSubject]:
    return await create_vehicle_archive_subjects_repo(subjects=subjects)


@brokers.broker.task
async def update_vehicle_archive_subjects_task(
    subjects: list[VehicleArchiveSubject],
) -> Sequence[VehicleArchiveSubject]:
    return await update_vehicle_archive_subjects_repo(subjects=subjects)


@brokers.broker.task
async def delete_vehicle_archive_subjects_task(archive_ids: list[str]) -> list[str]:
    return await delete_vehicle_archive_subjects_repo(archive_ids=archive_ids)
