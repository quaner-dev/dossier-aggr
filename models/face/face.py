from sqlalchemy import JSON, Column, UniqueConstraint
from sqlmodel import Field

from domain.face.face import Face as FaceDomain
from schemas import SubImageInfoList


class Face(FaceDomain, table=True):
    __table_args__ = (UniqueConstraint("FaceID"),)

    id: int | None = Field(default=None, primary_key=True, exclude=True)
    SubImageList: SubImageInfoList | None = Field(
        default=None, description="图像列表", sa_column=Column(JSON)
    )
