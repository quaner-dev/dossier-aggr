import asyncio
from types import ModuleType

import pytest

from core import settings
from repo.archive import archive_subject as archive_subject_repo
from repo.vehicle import vehicle_archive_subject as vehicle_archive_subject_repo


class _FailingBeginContext:
    async def __aenter__(self):
        raise AssertionError("runtime schema creation should not run outside dev")

    async def __aexit__(self, exc_type, exc, traceback):
        return False


class _FailingEngine:
    def begin(self):
        return _FailingBeginContext()


@pytest.mark.parametrize(
    "repo_module",
    [
        archive_subject_repo,
        vehicle_archive_subject_repo,
    ],
)
def test_schema_fallback_is_skipped_outside_dev(
    monkeypatch: pytest.MonkeyPatch,
    repo_module: ModuleType,
) -> None:
    monkeypatch.setattr(settings, "ENV", "prod")
    monkeypatch.setattr(repo_module, "_TABLE_READY", False)
    monkeypatch.setattr(repo_module, "engine", _FailingEngine())

    asyncio.run(repo_module._ensure_table())
