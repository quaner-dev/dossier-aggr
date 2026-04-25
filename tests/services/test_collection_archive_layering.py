import asyncio

from models import APE, APS, Archive, ArchiveLibrary, ArchiveQuery, VehicleArchive
from models.common import enums
from services.archive.archives import ArchiveService
from services.collection.ape import APEService
from services.collection.aps import APSService
from services.library.archive_library import ArchiveLibraryService
from services.vehicle.vehicle_archive import VehicleArchiveService
import services.archive.archives as archive_service_module
import services.collection.ape as ape_service_module
import services.collection.aps as aps_service_module
import services.library.archive_library as library_service_module
import services.vehicle.vehicle_archive as vehicle_service_module
import tasks.archive.archives as archive_task_module
import tasks.collection.ape as ape_task_module
import tasks.collection.aps as aps_task_module
import tasks.library.archive_library as library_task_module
import tasks.vehicle.vehicle_archive as vehicle_task_module
from tests.type_helpers import dt, sample_feature_info_list, sample_sub_image_list


def _sample_aps() -> APS:
    return APS(
        ApsID="APS-LAYER-001",
        Name="APS-Layer",
        IPAddr="192.168.1.10",
        IPV6Addr=None,
        Port=8000,
        IsOnline=enums.StatusTypeEnum.Online,
    )


def _sample_ape() -> APE:
    return APE(
        ApeID="APE-LAYER-001",
        Name="APE-Layer",
        Model="Model-X",
        IPAddr="192.168.1.11",
        IPV6Addr=None,
        Port=8080,
        Longitude=116.3913,
        Latitude=39.9075,
        PlaceCode="110000",
        Place="Beijing",
        OrgCode="110101",
        CapDirection=enums.CapDirectionEnum.Front,
        MonitorDirection=enums.MonitorDirectionEnum.WestToEast,
        MonitorAreaDesc="Gate",
        IsOnline=enums.StatusTypeEnum.Online,
        OwnerApsID="APS-LAYER-001",
        UserId="admin",
        Password="pass",
        FunctionType="Capture",
        PositionType="Fixed",
    )


def _sample_library() -> ArchiveLibrary:
    return ArchiveLibrary(
        ArchiveLibraryID="LIB-LAYER-001",
        Name="Lib-Layer",
        CreateTime=dt("20260101120000"),
        Memo=None,
    )


def _sample_archive() -> Archive:
    return Archive(
        ArchiveID="A-LAYER-001",
        ArchiveLibraryID="LIB-LAYER-001",
        CreateTime=dt("20260101120000"),
        UpdateTime=dt("20260101120000"),
        SourceIDList=["PERSON-LAYER-001", "FACE-LAYER-001"],
        CenterFeatureList=sample_feature_info_list("archive-layer"),
        Similaritydegree=0.91,
        Confidence=0.82,
        SubImageList=sample_sub_image_list(
            "IMG-LAYER-001", enums.ImageTypeEnum.PersonImage, "archive-layer"
        ),
    )


def _sample_vehicle_archive() -> VehicleArchive:
    return VehicleArchive(
        ArchiveID="VA-LAYER-001",
        ArchiveLibraryID="LIB-LAYER-001",
        PlateNo="A12345",
        PlateColor=enums.ColorTypeEnum.Blue,
        VehicleClass="K11",
        CreateTime=dt("20260101120000"),
        UpdateTime=dt("20260101120000"),
        SourceIDList=["MV-LAYER-001"],
        SubImageList=sample_sub_image_list(
            "IMG-VA-LAYER-001", enums.ImageTypeEnum.VehicleLargeImage, "vehicle-layer"
        ),
    )


def test_services_sync_reads_use_repositories(monkeypatch):
    async def _run():
        aps = _sample_aps()
        ape = _sample_ape()
        library = _sample_library()
        archive = _sample_archive()
        vehicle_archive = _sample_vehicle_archive()
        called = {
            "aps_repo": False,
            "ape_repo": False,
            "library_repo": False,
            "archive_repo": False,
            "vehicle_repo": False,
        }

        async def fake_list_apss_repo():
            called["aps_repo"] = True
            return [aps]

        async def fake_list_apes_repo():
            called["ape_repo"] = True
            return [ape]

        async def fake_list_archive_libraries_repo(filters: dict[str, str] | None = None):
            called["library_repo"] = True
            assert filters == {"ArchiveLibraryID": "LIB-LAYER-001"}
            return [library]

        async def fake_list_archives_repo():
            called["archive_repo"] = True
            return [archive]

        async def fake_query_vehicle_archives_repo(query: ArchiveQuery):
            called["vehicle_repo"] = True
            assert query.QueryID == "Q-VA-LAYER-001"
            return [vehicle_archive]

        monkeypatch.setattr(
            aps_service_module, "list_apss_repo", fake_list_apss_repo, raising=False
        )
        monkeypatch.setattr(
            ape_service_module, "list_apes_repo", fake_list_apes_repo, raising=False
        )
        monkeypatch.setattr(
            library_service_module,
            "list_archive_libraries_repo",
            fake_list_archive_libraries_repo,
            raising=False,
        )
        monkeypatch.setattr(
            archive_service_module, "list_archives_repo", fake_list_archives_repo, raising=False
        )
        monkeypatch.setattr(
            vehicle_service_module,
            "query_vehicle_archives_repo",
            fake_query_vehicle_archives_repo,
            raising=False,
        )

        aps_res = await APSService().list_apss()
        ape_res = await APEService().list_apes()
        library_res = await ArchiveLibraryService().list_archive_libraries(
            {"ArchiveLibraryID": "LIB-LAYER-001"}
        )
        archive_res = await ArchiveService().list_archives()
        vehicle_res = await VehicleArchiveService().query_vehicle_archives(
            ArchiveQuery(QueryID="Q-VA-LAYER-001")
        )

        assert aps_res[0].ApsID == "APS-LAYER-001"
        assert ape_res[0].ApeID == "APE-LAYER-001"
        assert library_res[0].ArchiveLibraryID == "LIB-LAYER-001"
        assert archive_res[0].ArchiveID == "A-LAYER-001"
        assert vehicle_res[0].ArchiveID == "VA-LAYER-001"
        assert all(called.values())

    asyncio.run(_run())


def test_aps_service_update_uses_kiq(monkeypatch):
    async def _run():
        called = {"dispatch": False}

        async def fake_dispatch(task, **kwargs):
            called["dispatch"] = True
            assert task is aps_service_module.update_aps_task
            assert kwargs == {"aps_id": "APS-LAYER-001"}
            return None

        monkeypatch.setattr(
            aps_service_module,
            "dispatch_and_wait",
            fake_dispatch,
            raising=False,
        )

        res = await APSService().update_aps("APS-LAYER-001")

        assert called["dispatch"] is True
        assert res == "APS-LAYER-001"

    asyncio.run(_run())


def test_tasks_delegate_to_repositories(monkeypatch):
    async def _run():
        aps = _sample_aps()
        ape = _sample_ape()
        library = _sample_library()
        archive = _sample_archive()
        vehicle_archive = _sample_vehicle_archive()
        called = {
            "aps_list_repo": False,
            "aps_update_repo": False,
            "ape_list_repo": False,
            "ape_update_repo": False,
            "library_list_repo": False,
            "library_delete_repo": False,
            "archive_list_repo": False,
            "archive_delete_repo": False,
            "vehicle_list_repo": False,
            "vehicle_delete_repo": False,
        }

        async def fake_list_apss_repo():
            called["aps_list_repo"] = True
            return [aps]

        async def fake_update_aps_repo(aps_id: str):
            called["aps_update_repo"] = True
            assert aps_id == "APS-LAYER-001"
            return aps

        async def fake_list_apes_repo():
            called["ape_list_repo"] = True
            return [ape]

        async def fake_update_apes_repo(apes: list[APE]):
            called["ape_update_repo"] = True
            assert len(apes) == 1
            return apes

        async def fake_list_archive_libraries_repo():
            called["library_list_repo"] = True
            return [library]

        async def fake_delete_archive_libraries_repo(library_ids: list[str]):
            called["library_delete_repo"] = True
            assert library_ids == ["LIB-LAYER-001"]
            return library_ids

        async def fake_list_archives_repo():
            called["archive_list_repo"] = True
            return [archive]

        async def fake_delete_archives_repo(archive_ids: list[str]):
            called["archive_delete_repo"] = True
            assert archive_ids == ["A-LAYER-001"]
            return archive_ids

        async def fake_list_vehicle_archives_repo():
            called["vehicle_list_repo"] = True
            return [vehicle_archive]

        async def fake_delete_vehicle_archives_repo(archive_ids: list[str]):
            called["vehicle_delete_repo"] = True
            assert archive_ids == ["VA-LAYER-001"]
            return archive_ids

        monkeypatch.setattr(aps_task_module, "list_apss_repo", fake_list_apss_repo, raising=False)
        monkeypatch.setattr(
            aps_task_module, "update_aps_repo", fake_update_aps_repo, raising=False
        )
        monkeypatch.setattr(ape_task_module, "list_apes_repo", fake_list_apes_repo, raising=False)
        monkeypatch.setattr(
            ape_task_module, "update_apes_repo", fake_update_apes_repo, raising=False
        )
        monkeypatch.setattr(
            library_task_module,
            "list_archive_libraries_repo",
            fake_list_archive_libraries_repo,
            raising=False,
        )
        monkeypatch.setattr(
            library_task_module,
            "delete_archive_libraries_repo",
            fake_delete_archive_libraries_repo,
            raising=False,
        )
        monkeypatch.setattr(
            archive_task_module, "list_archives_repo", fake_list_archives_repo, raising=False
        )
        monkeypatch.setattr(
            archive_task_module,
            "delete_archives_repo",
            fake_delete_archives_repo,
            raising=False,
        )
        monkeypatch.setattr(
            vehicle_task_module,
            "list_vehicle_archives_repo",
            fake_list_vehicle_archives_repo,
            raising=False,
        )
        monkeypatch.setattr(
            vehicle_task_module,
            "delete_vehicle_archives_repo",
            fake_delete_vehicle_archives_repo,
            raising=False,
        )

        aps_list_res = await aps_task_module.list_apss_task()
        aps_update_res = await aps_task_module.update_aps_task.original_func("APS-LAYER-001")
        ape_list_res = await ape_task_module.list_apes_task()
        ape_update_res = await ape_task_module.update_apes_task.original_func([ape])
        library_list_res = await library_task_module.list_archive_libraries_task()
        library_delete_res = await library_task_module.delete_archive_libraries_task.original_func(
            ["LIB-LAYER-001"]
        )
        archive_list_res = await archive_task_module.list_archives_task()
        archive_delete_res = await archive_task_module.delete_archives_task.original_func(
            ["A-LAYER-001"]
        )
        vehicle_list_res = await vehicle_task_module.list_vehicle_archives_task()
        vehicle_delete_res = await vehicle_task_module.delete_vehicle_archives_task.original_func(
            ["VA-LAYER-001"]
        )

        assert aps_list_res[0].ApsID == "APS-LAYER-001"
        assert aps_update_res.ApsID == "APS-LAYER-001"
        assert ape_list_res[0].ApeID == "APE-LAYER-001"
        assert ape_update_res[0].ApeID == "APE-LAYER-001"
        assert library_list_res[0].ArchiveLibraryID == "LIB-LAYER-001"
        assert library_delete_res == ["LIB-LAYER-001"]
        assert archive_list_res[0].ArchiveID == "A-LAYER-001"
        assert archive_delete_res == ["A-LAYER-001"]
        assert vehicle_list_res[0].ArchiveID == "VA-LAYER-001"
        assert vehicle_delete_res == ["VA-LAYER-001"]
        assert all(called.values())

    asyncio.run(_run())
