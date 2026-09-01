from sqlmodel import Field, SQLModel

from domain.common import Gait as GaitDomain

from .sub_image_info import SubImageInfoList


class Gait(GaitDomain):
    SubImageList: SubImageInfoList | None = Field(default=None, description="图片列表")


class GaitList(SQLModel):
    GaitObject: list[Gait]
