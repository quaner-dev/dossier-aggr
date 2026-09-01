from collections.abc import Sequence

from domain import VehicleArchive as VehicleArchiveData
from models import VehicleArchive
from repo.vehicle.vehicle_archive import (
    create_vehicle_archives_repo,
    delete_vehicle_archives_repo,
    list_vehicle_archives_repo,
    query_vehicle_archives_repo,
    update_vehicle_archives_repo,
)
from schemas import ArchiveQuery
from services.model_conversion import to_table_models


class VehicleArchiveService:
    """编排 GA/T 2350.5 A.11/A.12 车辆档案业务链路。

    查询、创建、更新和删除统一委托 repo。
    """

    async def query_vehicle_archives(self, query: ArchiveQuery) -> list[VehicleArchive]:
        return list(await query_vehicle_archives_repo(query=query))

    async def list_vehicle_archives(self) -> list[VehicleArchive]:
        return list(await list_vehicle_archives_repo())

    async def create_vehicle_archives(
        self, archives: Sequence[VehicleArchiveData]
    ) -> list[VehicleArchive]:
        return list(await create_vehicle_archives_repo(archives=to_table_models(VehicleArchive, archives)))

    async def update_vehicle_archives(
        self, archives: Sequence[VehicleArchiveData]
    ) -> list[VehicleArchive]:
        return list(await update_vehicle_archives_repo(archives=to_table_models(VehicleArchive, archives)))

    async def delete_vehicle_archives(self, archive_ids: list[str]) -> list[str]:
        return await delete_vehicle_archives_repo(archive_ids=archive_ids)
