from repositories.verify.vehicle_archive_confidence import (
    verify_vehicle_archive_confidence_repo,
)


async def verify_vehicle_archive_confidence_task(archive_ids: list[str]) -> list[str]:
    return await verify_vehicle_archive_confidence_repo(archive_ids=archive_ids)
