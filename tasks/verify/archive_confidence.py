from repo.verify.archive_confidence import verify_archive_confidence_repo


async def verify_archive_confidence_task(archive_ids: list[str]) -> list[str]:
    return await verify_archive_confidence_repo(archive_ids=archive_ids)
