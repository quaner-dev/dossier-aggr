from models import VehicleArchive
from repo.verify.vehicle_archive_confidence import (
    verify_vehicle_archive_confidence_repo,
)


class VehicleArchiveConfidenceService:
    async def verify_vehicle_archive_confidence(
        self, archives: list[VehicleArchive]
    ) -> list[VehicleArchive]:
        return await verify_vehicle_archive_confidence_repo(archives=archives)
