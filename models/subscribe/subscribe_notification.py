from sqlalchemy import JSON, Column, UniqueConstraint
from sqlmodel import Field

from domain.subscribe.subscribe_notification import (
    SubscribeNotification as SubscribeNotificationDomain,
)
from schemas import (
    ArchiveList,
    ArchiveSubjectList,
    FaceList,
    PersonList,
    VehicleArchiveList,
)


class SubscribeNotification(SubscribeNotificationDomain, table=True):
    __table_args__ = (UniqueConstraint("NotificationID"),)

    id: int | None = Field(default=None, primary_key=True, exclude=True)
    ArchiveObjectList: ArchiveList | None = Field(default=None, sa_column=Column(JSON))
    VehicleArchiveObjectList: VehicleArchiveList | None = Field(default=None, sa_column=Column(JSON))
    ArchiveSubjectList: ArchiveSubjectList | None = Field(default=None, sa_column=Column(JSON))
    FaceObjectList: FaceList | None = Field(default=None, sa_column=Column(JSON))
    PersonObjectList: PersonList | None = Field(default=None, sa_column=Column(JSON))
