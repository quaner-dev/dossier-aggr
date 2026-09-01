from domain import Subscribe
from schemas import SubscribeNotification


def test_2350_a7_subscribe_reuse_fields_present():
    fields = set(Subscribe.model_fields.keys())

    expected = {
        "SubscribeID",
        "SubscribeDetail",
        "ResourceURI",
        "BeginTime",
        "EndTime",
        "ReceiveAddr",
        "OperateType",
        "SubscribeStatus",
        "ResultImageDeclare",
        "ResultFeatureDeclare",
    }

    for field in expected:
        assert field in fields


def test_2350_a8_subscribe_notification_reuse_fields_present():
    fields = set(SubscribeNotification.model_fields.keys())

    expected = {
        "NotificationID",
        "SubscribeID",
        "TriggerTime",
        "InfoIDs",
        "DeviceList",
        "DataClassTabObjectList",
        "ArchiveObjectList",
        "VehicleArchiveObjectList",
        "ArchiveSubjectList",
        "ExecuteOperation",
    }

    for field in expected:
        assert field in fields
