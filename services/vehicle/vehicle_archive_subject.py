from models import VehicleArchiveSubject
from repositories.vehicle.vehicle_archive_subject import (
    query_vehicle_archive_subjects_repo,
)
from tasks.vehicle.vehicle_archive_subject import (
    create_vehicle_archive_subjects_task,
    update_vehicle_archive_subjects_task,
    delete_vehicle_archive_subjects_task,
)
from services.task_dispatch import dispatch_and_wait


class VehicleArchiveSubjectService:
    async def query_vehicle_archive_subjects(self) -> list[VehicleArchiveSubject]:
        return list(await query_vehicle_archive_subjects_repo())

    async def create_vehicle_archive_subjects(
        self, subjects: list[VehicleArchiveSubject]
    ) -> list[VehicleArchiveSubject]:
        return await dispatch_and_wait(
            create_vehicle_archive_subjects_task,
            subjects=subjects,
        )

    async def update_vehicle_archive_subjects(
        self, subjects: list[VehicleArchiveSubject]
    ) -> list[VehicleArchiveSubject]:
        return await dispatch_and_wait(
            update_vehicle_archive_subjects_task,
            subjects=subjects,
        )

    async def delete_vehicle_archive_subjects(self, archive_ids: list[str]) -> list[str]:
        return await dispatch_and_wait(
            delete_vehicle_archive_subjects_task,
            archive_ids=archive_ids,
        )
