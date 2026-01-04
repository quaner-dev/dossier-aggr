from sqlmodel import Field, SQLModel  # type: ignore

import base


class SubscribeNotificationFaceLink(SQLModel, table=True):
    NotificationID: str = Field(
        foreign_key="subscribenotification.NotificationID", primary_key=True
    )
    FaceID: str = Field(foreign_key="face.FaceID", primary_key=True, unique=True)


class SubscribeNotificationPersonLink(SQLModel, table=True):
    NotificationID: str = Field(
        foreign_key="subscribenotification.NotificationID", primary_key=True
    )
    PersonID: str = Field(foreign_key="person.PersonID", primary_key=True, unique=True)


class SubscribeNotification(
    base.subscribe_notification.SubscribeNotificationBase, table=True
): ...
