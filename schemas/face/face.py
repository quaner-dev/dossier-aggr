from sqlmodel import Field, SQLModel

from domain.face import Face as FaceDomain

from ..common.sub_image_info import SubImageInfoList


class Face(FaceDomain):
    SubImageList: SubImageInfoList | None = Field(default=None, description="图像列表")


class FaceList(SQLModel):
    FaceObject: list[Face]


class FaceListObjectSchema(SQLModel):
    FaceListObject: FaceList


class FaceQueryParams(SQLModel):
    RecordStartNo: int = Field(default=0, ge=0, description="起始记录号")
    PageRecordNum: int | None = Field(default=None, ge=1, description="本页记录数")
