from collections.abc import Sequence

import brokers
from models import VehicleArchive
from repo.vehicle.vehicle_archive import (
    create_vehicle_archives_repo,
    delete_vehicle_archives_repo,
    list_vehicle_archives_repo,
    update_vehicle_archives_repo,
)


async def list_vehicle_archives_task() -> Sequence[VehicleArchive]:
    return await list_vehicle_archives_repo()


@brokers.broker.task
async def create_vehicle_archives_task(
    archives: list[VehicleArchive],
) -> Sequence[VehicleArchive]:
    return await create_vehicle_archives_repo(archives=archives)


@brokers.broker.task
async def update_vehicle_archives_task(
    archives: list[VehicleArchive],
) -> Sequence[VehicleArchive]:
    return await update_vehicle_archives_repo(archives=archives)


@brokers.broker.task
async def delete_vehicle_archives_task(archive_ids: list[str]) -> list[str]:
    return await delete_vehicle_archives_repo(archive_ids=archive_ids)
