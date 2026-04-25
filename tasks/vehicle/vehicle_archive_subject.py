from collections.abc import Sequence

from core import brokers
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
async def delete_vehicle_archive_subjects_task(
    archive_id: str | None = None,
    face_id_list: list[str] | None = None,
    person_id_list: list[str] | None = None,
    motor_vehicle_id_list: list[str] | None = None,
    non_motor_vehicle_id_list: list[str] | None = None,
) -> list[str]:
    return await delete_vehicle_archive_subjects_repo(
        archive_id=archive_id,
        face_id_list=face_id_list,
        person_id_list=person_id_list,
        motor_vehicle_id_list=motor_vehicle_id_list,
        non_motor_vehicle_id_list=non_motor_vehicle_id_list,
    )
