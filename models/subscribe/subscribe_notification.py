from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field

from ..archive.archive import ArchiveList
from ..archive.archive_subject import ArchiveSubjectList as ArchiveSubjectPayloadList
from ..archive.vehicle_archive import VehicleArchiveList
from ..common import enums
from ..face.face import FaceList
from ..person.person import PersonList


class SubscribeNotification(SQLModel, table=True):
    """GA/T 1400.3-2017 A.20 通知对象"""

    id: int | None = Field(default=None, primary_key=True, exclude=True)

    NotificationID: str = Field(description="通知标识", max_length=33, unique=True)
    SubscribeID: str = Field(description="订阅标识", max_length=33)
    Title: str = Field(description="订阅标题", max_length=256)
    TriggerTime: str = Field(description="触发时间")
    InfoIDs: str = Field(description="信息标识", max_length=1024)
    DeviceList: str | None = Field(default=None, description="设备")
    DataClassTabObjectList: str | None = Field(default=None, description="数据分类标签")
    ExecuteOperation: enums.ExecuteOperationEnum | None = Field(
        default=None, description="更新项目"
    )

    ArchiveObjectList: ArchiveList | None = Field(
        default=None, description="人员基础档案信息", sa_column=Column(JSON)
    )
    VehicleArchiveObjectList: VehicleArchiveList | None = Field(
        default=None, description="车辆基础档案信息", sa_column=Column(JSON)
    )
    ArchiveSubjectList: ArchiveSubjectPayloadList | None = Field(
        default=None, description="档案明细信息", sa_column=Column(JSON)
    )
    FaceObjectList: FaceList | None = Field(
        default=None, description="人脸信息", sa_column=Column(JSON)
    )
    PersonObjectList: PersonList | None = Field(
        default=None, description="人员信息", sa_column=Column(JSON)
    )


class SubscribeNotificationList(SQLModel):
    """GA/T 1400.3-2017 C.20 通知对象列表"""

    SubscribeNotificationObject: list[SubscribeNotification]


# 通知对象列表结构
class SubscribeNotificationListSchema(SQLModel):
    SubscribeNotificationListObject: SubscribeNotificationList
