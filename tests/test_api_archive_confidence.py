import asyncio

from api.verify.archive_confidence import archive_confidence_verify
from tests.type_helpers import as_service, as_status_list


class _FakeArchiveConfidenceService:
    def __init__(self):
        self.called_with: list[str] | None = None

    async def verify_archive_confidence(self, archive_ids: list[str]):
        self.called_with = archive_ids
        return archive_ids


def test_archive_confidence_returns_status_list():
    async def _run():
        fake = _FakeArchiveConfidenceService()
        res = await archive_confidence_verify(
            archive_ids=["A-001", "A-002"], service=as_service(fake)
        )

        status = as_status_list(res.ResponseStatusListObject.ResponseStatusObject)
        assert len(status) == 2
        assert status[0].Id == "A-001"
        assert status[0].StatusCode == "0"
        assert fake.called_with == ["A-001", "A-002"]

    asyncio.run(_run())
