from models import VehicleArchive
from repo.verify.vehicle_archive_confidence import (
    verify_vehicle_archive_confidence_repo,
)


async def verify_vehicle_archive_confidence_task(
    archives: list[VehicleArchive],
) -> list[VehicleArchive]:
    return await verify_vehicle_archive_confidence_repo(archives=archives)
