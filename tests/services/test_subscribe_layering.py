import asyncio

from models import Subscribe, SubscribeNotification
from models.common import enums
from services.subscribe.subscribe import SubscribeService
from services.subscribe.subscribe_notification import SubscribeNotificationService
import services.subscribe.subscribe as subscribe_service_module
import services.subscribe.subscribe_notification as notification_service_module
import tasks.subscribe.subscribe as subscribe_task_module
import tasks.subscribe.subscribe_notification as notification_task_module


def _sample_subscribe() -> Subscribe:
    return Subscribe(
        SubscribeID="S-LAYER-001",
        Title="Layering",
        SubscribeDetail="face",
        ResourceClass=enums.ResourceClassEnum.Ape,
        ResourceURI="/VIID/Faces",
        ApplicantName="tester",
        ApplicantOrg="org",
        BeginTime="20260101120000",
        EndTime="20270101120000",
        ReceiveAddr="http://127.0.0.1/callback",
        ReportInterval=30,
        Reason=None,
        OperateType=enums.OperateTypeEnum.Subscribe,
        SubscribeStatus=enums.SubscribeStatusEnum.Active,
        SubscribeCancelOrg=None,
        SubscribeCancelPerson=None,
        CancelTime=None,
        CancelReason=None,
        ResultImageDeclare=enums.ResultImageDeclareEnum.FaceImage,
        ResultFeatureDeclare=enums.ResultFeatureDeclareEnum.WithFeatures,
        TabID=None,
    )


def _sample_notification() -> SubscribeNotification:
    return SubscribeNotification(
        NotificationID="N-LAYER-001",
        SubscribeID="S-LAYER-001",
        Title="Layering",
        TriggerTime="20260101120000",
        InfoIDs="P-001,F-001",
        DeviceList=None,
        DataClassTabObjectList=None,
        ExecuteOperation=None,
        FaceObjectList=None,
        PersonObjectList=None,
    )


def test_subscribe_service_sync_reads_use_repository(monkeypatch):
    async def _run():
        subscribe = _sample_subscribe()
        called = {"list": False, "get": False}

        async def fake_list_repo():
            called["list"] = True
            return [subscribe]

        async def fake_get_repo(subscribe_id: str):
            called["get"] = True
            assert subscribe_id == "S-LAYER-001"
            return subscribe

        monkeypatch.setattr(
            subscribe_service_module,
            "list_subscribes_repo",
            fake_list_repo,
            raising=False,
        )
        monkeypatch.setattr(
            subscribe_service_module,
            "get_subscribe_repo",
            fake_get_repo,
            raising=False,
        )
        # Service sync-read path should not call task layer.
        monkeypatch.setattr(
            subscribe_service_module,
            "list_subscribes_task",
            lambda *args, **kwargs: (_ for _ in ()).throw(
                AssertionError("list_subscribes_task should not be called")
            ),
            raising=False,
        )
        monkeypatch.setattr(
            subscribe_service_module,
            "get_subscribe_task",
            lambda *args, **kwargs: (_ for _ in ()).throw(
                AssertionError("get_subscribe_task should not be called")
            ),
            raising=False,
        )

        service = SubscribeService()
        list_res = await asyncio.wait_for(service.list_subscribes(), timeout=1)
        get_res = await asyncio.wait_for(
            service.get_subscribe("S-LAYER-001"), timeout=1
        )

        assert called["list"] is True
        assert called["get"] is True
        assert list_res[0].SubscribeID == "S-LAYER-001"
        assert get_res.SubscribeID == "S-LAYER-001"

    asyncio.run(_run())


def test_subscribe_notification_service_sync_read_uses_repository(monkeypatch):
    async def _run():
        notification = _sample_notification()
        called = {"list": False}

        async def fake_list_repo(filters: dict[str, str] | None = None):
            called["list"] = True
            assert filters == {"NotificationID": "N-LAYER-001"}
            return [notification]

        monkeypatch.setattr(
            notification_service_module,
            "list_subscribe_notifications_repo",
            fake_list_repo,
            raising=False,
        )
        # Service sync-read path should not call task layer.
        monkeypatch.setattr(
            notification_service_module,
            "list_subscribe_notifications_task",
            lambda *args, **kwargs: (_ for _ in ()).throw(
                AssertionError("list_subscribe_notifications_task should not be called")
            ),
            raising=False,
        )

        service = SubscribeNotificationService()
        res = await asyncio.wait_for(
            service.list_subscribe_notifications({"NotificationID": "N-LAYER-001"}),
            timeout=1,
        )

        assert called["list"] is True
        assert res[0].NotificationID == "N-LAYER-001"

    asyncio.run(_run())


def test_subscribe_tasks_delegate_to_repository(monkeypatch):
    async def _run():
        subscribe = _sample_subscribe()
        notification = _sample_notification()
        called = {
            "list_subscribe": False,
            "get_subscribe": False,
            "list_notification": False,
            "delete_notification": False,
        }

        async def fake_list_repo():
            called["list_subscribe"] = True
            return [subscribe]

        async def fake_get_repo(subscribe_id: str):
            called["get_subscribe"] = True
            assert subscribe_id == "S-LAYER-001"
            return subscribe

        async def fake_list_notification_repo(filters: dict[str, str] | None = None):
            called["list_notification"] = True
            assert filters == {"NotificationID": "N-LAYER-001"}
            return [notification]

        async def fake_delete_notification_repo(notification_ids: list[str]):
            called["delete_notification"] = True
            assert notification_ids == ["N-LAYER-001"]
            return notification_ids

        monkeypatch.setattr(
            subscribe_task_module, "list_subscribes_repo", fake_list_repo, raising=False
        )
        monkeypatch.setattr(
            subscribe_task_module, "get_subscribe_repo", fake_get_repo, raising=False
        )
        monkeypatch.setattr(
            notification_task_module,
            "list_subscribe_notifications_repo",
            fake_list_notification_repo,
            raising=False,
        )
        monkeypatch.setattr(
            notification_task_module,
            "delete_subscribe_notifications_repo",
            fake_delete_notification_repo,
            raising=False,
        )
        # Task layer should delegate to repositories, not open DB sessions directly.
        monkeypatch.setattr(
            subscribe_task_module,
            "AsyncSession",
            lambda *args, **kwargs: (_ for _ in ()).throw(
                AssertionError("AsyncSession should not be used in subscribe tasks")
            ),
            raising=False,
        )
        monkeypatch.setattr(
            notification_task_module,
            "AsyncSession",
            lambda *args, **kwargs: (_ for _ in ()).throw(
                AssertionError("AsyncSession should not be used in notification tasks")
            ),
            raising=False,
        )

        list_res = await asyncio.wait_for(
            subscribe_task_module.list_subscribes_task(), timeout=1
        )
        get_res = await asyncio.wait_for(
            subscribe_task_module.get_subscribe_task("S-LAYER-001"), timeout=1
        )
        n_res = await asyncio.wait_for(
            notification_task_module.list_subscribe_notifications_task(
                {"NotificationID": "N-LAYER-001"}
            ),
            timeout=1,
        )
        delete_notification_res = await asyncio.wait_for(
            notification_task_module.delete_subscribe_notifications_task.original_func(
                notification_ids=["N-LAYER-001"]
            ),
            timeout=1,
        )

        assert called["list_subscribe"] is True
        assert called["get_subscribe"] is True
        assert called["list_notification"] is True
        assert called["delete_notification"] is True
        assert list_res[0].SubscribeID == "S-LAYER-001"
        assert get_res.SubscribeID == "S-LAYER-001"
        assert n_res[0].NotificationID == "N-LAYER-001"
        assert delete_notification_res == ["N-LAYER-001"]

    asyncio.run(_run())
