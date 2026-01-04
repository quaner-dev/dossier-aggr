from sqlmodel import Field, SQLModel  # type: ignore

import base


class FaceSubImageInfoLink(SQLModel, table=True):
    FaceID: str = Field(foreign_key="face.FaceID", primary_key=True)
    ImageID: str = Field(
        foreign_key="subimageinfo.ImageID", primary_key=True, unique=True
    )


class Face(base.face.FaceBase, table=True): ...
