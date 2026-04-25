from models import Archive
from repo.verify.archive_confidence import verify_archive_confidence_repo


async def verify_archive_confidence_task(archives: list[Archive]) -> list[Archive]:
    return await verify_archive_confidence_repo(archives=archives)
