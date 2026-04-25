from models import Archive
from repo.verify.archive_confidence import verify_archive_confidence_repo


class ArchiveConfidenceService:
    async def verify_archive_confidence(self, archives: list[Archive]) -> list[Archive]:
        return await verify_archive_confidence_repo(archives=archives)
