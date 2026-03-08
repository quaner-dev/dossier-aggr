import asyncio

from api.verify.vehicle_archive_confidence import vehicle_archive_confidence_verify
from tests.type_helpers import as_service, as_status_list


class _FakeVehicleArchiveConfidenceService:
    def __init__(self):
        self.called_with: list[str] | None = None

    async def verify_vehicle_archive_confidence(self, archive_ids: list[str]):
        self.called_with = archive_ids
        return archive_ids


def test_vehicle_archive_confidence_returns_status_list():
    async def _run():
        fake = _FakeVehicleArchiveConfidenceService()
        res = await vehicle_archive_confidence_verify(
            archive_ids=["VA-001", "VA-002"], service=as_service(fake)
        )

        status = as_status_list(res.ResponseStatusListObject.ResponseStatusObject)
        assert len(status) == 2
        assert status[0].Id == "VA-001"
        assert status[0].StatusCode == "0"
        assert fake.called_with == ["VA-001", "VA-002"]

    asyncio.run(_run())
