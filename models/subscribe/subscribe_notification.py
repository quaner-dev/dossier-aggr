from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field

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
