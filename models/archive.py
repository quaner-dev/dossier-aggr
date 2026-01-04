from sqlmodel import Field, SQLModel  # type: ignore

import base


class ArchiveSubImageInfoLink(SQLModel, table=True):
    ArchiveID: str = Field(foreign_key="archive.ArchiveID", primary_key=True)
    ImageID: str = Field(
        foreign_key="subimageinfo.ImageID", primary_key=True, unique=True
    )


class Archive(base.archive.ArchiveBase, table=True): ...
