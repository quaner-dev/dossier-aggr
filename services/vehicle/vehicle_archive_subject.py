from models import ArchiveSubjectQuery, VehicleArchiveSubject
from repo.vehicle.vehicle_archive_subject import (
    create_vehicle_archive_subjects_repo,
    delete_vehicle_archive_subjects_repo,
    query_vehicle_archive_subjects_repo,
    update_vehicle_archive_subjects_repo,
)


class VehicleArchiveSubjectService:
    """编排 GA/T 2350.5 A.15/A.16 车辆档案明细业务链路。

    查询、创建、更新和删除统一委托 repo。
    """

    async def query_vehicle_archive_subjects(
        self, query: ArchiveSubjectQuery | None = None
    ) -> list[VehicleArchiveSubject]:
        return list(await query_vehicle_archive_subjects_repo(query=query))

    async def create_vehicle_archive_subjects(
        self, subjects: list[VehicleArchiveSubject]
    ) -> list[VehicleArchiveSubject]:
        return list(await create_vehicle_archive_subjects_repo(subjects=subjects))

    async def update_vehicle_archive_subjects(
        self, subjects: list[VehicleArchiveSubject]
    ) -> list[VehicleArchiveSubject]:
        return list(await update_vehicle_archive_subjects_repo(subjects=subjects))

    async def delete_vehicle_archive_subjects(
        self,
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
