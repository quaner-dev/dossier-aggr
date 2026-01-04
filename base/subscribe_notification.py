from sqlmodel import Field, SQLModel  # type: ignore

import base.enums as enums


class SubscribeNotificationBase(SQLModel):
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
