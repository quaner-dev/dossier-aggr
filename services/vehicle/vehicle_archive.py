from models import ArchiveQuery, VehicleArchive
from repo.vehicle.vehicle_archive import (
    list_vehicle_archives_repo,
    query_vehicle_archives_repo,
)
from tasks.vehicle.vehicle_archive import (
    create_vehicle_archives_task,
    update_vehicle_archives_task,
    delete_vehicle_archives_task,
)
from services.task_dispatch import dispatch_and_wait


class VehicleArchiveService:
    """编排 GA/T 2350.5 A.11/A.12 车辆档案业务链路。

    同步查询保留在 repo 层实现筛选语义；写操作统一投递 Taskiq task，
    使 service 只承担协议对象到业务动作的编排职责。
    """

    async def query_vehicle_archives(self, query: ArchiveQuery) -> list[VehicleArchive]:
        return list(await query_vehicle_archives_repo(query=query))

    async def list_vehicle_archives(self) -> list[VehicleArchive]:
        return list(await list_vehicle_archives_repo())

    async def create_vehicle_archives(
        self, archives: list[VehicleArchive]
    ) -> list[VehicleArchive]:
        return list(await dispatch_and_wait(create_vehicle_archives_task, archives=archives))

    async def update_vehicle_archives(
        self, archives: list[VehicleArchive]
    ) -> list[VehicleArchive]:
        return list(await dispatch_and_wait(update_vehicle_archives_task, archives=archives))

    async def delete_vehicle_archives(self, archive_ids: list[str]) -> list[str]:
        return await dispatch_and_wait(
            delete_vehicle_archives_task,
            archive_ids=archive_ids,
        )
