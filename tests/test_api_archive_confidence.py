import asyncio

from api.verify.archive_confidence import archive_confidence_verify
from domain.common import enums
from schemas import Archive, ArchiveList, ArchiveListSchema
from tests.type_helpers import (
    as_service,
    dt,
    sample_feature_info_list,
    sample_sub_image_list,
)


class _FakeArchiveConfidenceService:
    def __init__(self):
        self.called_with: list[Archive] | None = None

    async def verify_archive_confidence(self, archives: list[Archive]):
        self.called_with = archives
        return archives


def test_archive_confidence_returns_archive_list():
    async def _run():
        fake = _FakeArchiveConfidenceService()
        archives = [
            Archive(
                ArchiveID="A-001",
                ArchiveLibraryID="LIB-001",
                CreateTime=dt("20260101120000"),
                UpdateTime=dt("20260101120000"),
                SourceIDList=["PERSON-001", "FACE-001"],
                CenterFeatureList=sample_feature_info_list("a-001"),
                Similaritydegree=0.91,
                Confidence=0.82,
                SubImageList=sample_sub_image_list(
                    "IMG-A-001", enums.ImageTypeEnum.PersonImage, "a-001"
                ),
            ),
            Archive(
                ArchiveID="A-002",
                ArchiveLibraryID="LIB-001",
                CreateTime=dt("20260102120000"),
                UpdateTime=dt("20260102120000"),
                SourceIDList=["PERSON-002"],
                CenterFeatureList=sample_feature_info_list("a-002"),
                Similaritydegree=0.92,
                Confidence=0.83,
                SubImageList=sample_sub_image_list(
                    "IMG-A-002", enums.ImageTypeEnum.PersonImage, "a-002"
                ),
            ),
        ]
        payload = ArchiveListSchema(ArchiveListObject=ArchiveList(ArchiveObject=archives))
        res = await archive_confidence_verify(
            data=payload,
            service=as_service(fake),
        )

        returned_archives = res.ArchiveListObject.ArchiveObject
        assert len(returned_archives) == 2
        assert returned_archives[0].ArchiveID == "A-001"
        assert returned_archives[0].SubImageList.SubImageInfoObject[0].ImageID == "IMG-A-001"
        assert fake.called_with is not None
        assert fake.called_with[0].ArchiveID == "A-001"

    asyncio.run(_run())
