import asyncio
from typing import Any, cast

from services.collection.ape import APEService
from services.collection.aps import APSService
from services.library.archive_library import ArchiveLibraryService
from services.subscribe.subscribe import SubscribeService
from services.task.archive_task import ArchiveTaskService


def test_control_writes_call_repositories_directly(monkeypatch):
    async def _run() -> None:
        import services.collection.ape as ape_service_module
        import services.collection.aps as aps_service_module
        import services.library.archive_library as library_service_module
        import services.subscribe.subscribe as subscribe_service_module
        import services.task.archive_task as archive_task_service_module

        for module in (
            ape_service_module,
            library_service_module,
            subscribe_service_module,
            archive_task_service_module,
        ):
            monkeypatch.setattr(module, "to_table_models", lambda _, values: values)

        value = cast(Any, object())
        values = cast(list[Any], [value])
        calls: list[str] = []

        async def fake_update_apes_repo(*, apes: list[Any]) -> list[Any]:
            calls.append("ape")
            return apes

        async def fake_update_aps_repo(*, aps_id: str) -> Any:
            calls.append("aps")
            assert aps_id == "APS-001"
            return value

        async def fake_create_libraries_repo(*, libraries: list[Any]) -> list[Any]:
            calls.append("library")
            return libraries

        async def fake_create_subscribes_repo(*, subscribes: list[Any]) -> list[Any]:
            calls.append("subscribe")
            return subscribes

        async def fake_create_tasks_repo(*, tasks: list[Any]) -> list[Any]:
            calls.append("archive_task")
            return tasks

        monkeypatch.setattr(ape_service_module, "update_apes_repo", fake_update_apes_repo)
        monkeypatch.setattr(aps_service_module, "update_aps_repo", fake_update_aps_repo)
        monkeypatch.setattr(
            library_service_module,
            "create_archive_libraries_repo",
            fake_create_libraries_repo,
        )
        monkeypatch.setattr(
            subscribe_service_module,
            "create_subscribes_repo",
            fake_create_subscribes_repo,
        )
        monkeypatch.setattr(
            archive_task_service_module,
            "create_archive_tasks_repo",
            fake_create_tasks_repo,
        )

        assert await APEService().update_apes(values) is values
        assert await APSService().update_aps("APS-001") == "APS-001"
        assert await ArchiveLibraryService().create_archive_libraries(values) == values
        assert await SubscribeService().create_subscribes(values) == values
        assert await ArchiveTaskService().create_archive_tasks(values) == values
        assert calls == ["ape", "aps", "library", "subscribe", "archive_task"]

    asyncio.run(_run())
