from models import ArchiveSubjectQuery, VehicleArchiveSubject
from repo.vehicle.vehicle_archive_subject import (
    query_vehicle_archive_subjects_repo,
)
from tasks.vehicle.vehicle_archive_subject import (
    create_vehicle_archive_subjects_task,
    update_vehicle_archive_subjects_task,
    delete_vehicle_archive_subjects_task,
)
from services.task_dispatch import dispatch_and_wait


class VehicleArchiveSubjectService:
    async def query_vehicle_archive_subjects(
        self, query: ArchiveSubjectQuery | None = None
    ) -> list[VehicleArchiveSubject]:
        return list(await query_vehicle_archive_subjects_repo(query=query))

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

    async def delete_vehicle_archive_subjects(
        self,
        archive_id: str | None = None,
        face_id_list: list[str] | None = None,
        person_id_list: list[str] | None = None,
        motor_vehicle_id_list: list[str] | None = None,
        non_motor_vehicle_id_list: list[str] | None = None,
    ) -> list[str]:
        return await dispatch_and_wait(
            delete_vehicle_archive_subjects_task,
            archive_id=archive_id,
            face_id_list=face_id_list,
            person_id_list=person_id_list,
            motor_vehicle_id_list=motor_vehicle_id_list,
            non_motor_vehicle_id_list=non_motor_vehicle_id_list,
        )
