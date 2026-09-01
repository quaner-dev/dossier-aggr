from sqlmodel import Field, SQLModel

from domain.subscribe import SubscribeNotification as SubscribeNotificationDomain

from ..archive import (
    ArchiveList,
    ArchiveSubjectList,
    VehicleArchiveList,
)
from ..face import FaceList
from ..person import PersonList


class SubscribeNotification(SubscribeNotificationDomain):
    ArchiveObjectList: ArchiveList | None = Field(
        default=None, description="人员基础档案信息"
    )
    VehicleArchiveObjectList: VehicleArchiveList | None = Field(
        default=None, description="车辆基础档案信息"
    )
    ArchiveSubjectList: ArchiveSubjectList | None = Field(
        default=None, description="档案明细信息"
    )
    FaceObjectList: FaceList | None = Field(default=None, description="人脸信息")
    PersonObjectList: PersonList | None = Field(default=None, description="人员信息")


class SubscribeNotificationList(SQLModel):
    SubscribeNotificationObject: list[SubscribeNotification]


class SubscribeNotificationListSchema(SQLModel):
    SubscribeNotificationListObject: SubscribeNotificationList
