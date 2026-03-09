import asyncio

import pytest
from taskiq import InMemoryBroker

import brokers
import settings
from models import ArchiveSubject
from repo.archive.archive_subject import delete_archive_subjects_repo
from services.archive.archive_subject import ArchiveSubjectService


pytestmark = pytest.mark.skipif(
    (
        not isinstance(brokers.broker, InMemoryBroker)
        or settings.DATABASE_URL.startswith("sqlite+aiosqlite")
    ),
    reason=(
        "This e2e test requires Taskiq InMemoryBroker and a non-aiosqlite "
        "async database backend in current test environment"
    ),
)


def _sample_subjects() -> list[ArchiveSubject]:
    return [
        ArchiveSubject(
            ArchiveID="AS-E2E-001",
            PersonIDList=["P-E2E-001"],
            FaceIDList=["F-E2E-001"],
            PersonObjectList=None,
            FaceObjectList=None,
            ImageID="IMG-AS-E2E-001",
        ),
        ArchiveSubject(
            ArchiveID="AS-E2E-002",
            PersonIDList=["P-E2E-002"],
            FaceIDList=["F-E2E-002"],
            PersonObjectList=None,
            FaceObjectList=None,
            ImageID="IMG-AS-E2E-002",
        ),
    ]


async def _cleanup_subjects_by_id(archive_ids: list[str]) -> None:
    for archive_id in archive_ids:
        await delete_archive_subjects_repo(archive_id=archive_id)


async def _wait_until(predicate, timeout_seconds: float = 5.0, interval_seconds: float = 0.05):
    deadline = asyncio.get_running_loop().time() + timeout_seconds
    while asyncio.get_running_loop().time() < deadline:
        if await predicate():
            return True
        await asyncio.sleep(interval_seconds)
    return False


def test_async_write_is_eventually_visible_after_taskiq_dispatch():
    async def _run():
        await brokers.broker.startup()
        try:
            service = ArchiveSubjectService()
            subjects = _sample_subjects()
            archive_ids = [subject.ArchiveID for subject in subjects]
            await _cleanup_subjects_by_id(archive_ids)

            # Create path uses .kiq asynchronous dispatch.
            _ = await service.create_archive_subjects(subjects=subjects)

            async def _is_visible() -> bool:
                try:
                    queried = await service.query_archive_subjects()
                except Exception:
                    return False
                queried_ids = {subject.ArchiveID for subject in queried}
                return {"AS-E2E-001", "AS-E2E-002"}.issubset(queried_ids)

            assert await _wait_until(_is_visible, timeout_seconds=5.0)
        finally:
            await _cleanup_subjects_by_id(["AS-E2E-001", "AS-E2E-002"])
            await brokers.broker.shutdown()

    asyncio.run(_run())
