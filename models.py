from sqlmodel import Field, SQLModel # type: ignore

import base


class APS(base.APSBase, table=True): ...


class APE(base.APEBase, table=True): ...


class SubImageInfo(base.SubImageInfoBase, table=True): ...


class FeatureInfo(base.FeatureInfoBase, table=True): ...


class PersonSubImageInfoLink(SQLModel, table=True):
    PersonID: str = Field(foreign_key="person.PersonID", primary_key=True)
    ImageID: str = Field(
        foreign_key="subimageinfo.ImageID", primary_key=True, unique=True
    )


class Person(base.PersonBase, table=True): ...


class FaceSubImageInfoLink(SQLModel, table=True):
    FaceID: str = Field(foreign_key="face.FaceID", primary_key=True)
    ImageID: str = Field(
        foreign_key="subimageinfo.ImageID", primary_key=True, unique=True
    )


class Face(base.FaceBase, table=True): ...


class Subscribe(base.SubscribeBase, table=True): ...


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


class SubscribeNotification(base.SubscribeNotificationBase, table=True): ...


class ArchiveSubImageInfoLink(SQLModel, table=True):
    ArchiveID: str = Field(foreign_key="archive.ArchiveID", primary_key=True)
    ImageID: str = Field(
        foreign_key="subimageinfo.ImageID", primary_key=True, unique=True
    )


class Archive(base.ArchiveBase, table=True):...
