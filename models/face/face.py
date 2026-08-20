from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel

from ..common import enums
from ..common.sub_image_info import SubImageInfoList


class Face(SQLModel, table=True):
    """GA/T 1400.3-2017 A.9 人脸对象"""

    id: int | None = Field(default=None, primary_key=True, exclude=True)

    FaceID: str = Field(description="人脸标识", max_length=33, unique=True)
    InfoKind: enums.InfoKindEnum = Field(
        default=enums.InfoKindEnum.Other, description="信息分类"
    )
    SourceID: str = Field(description="来源标识", max_length=41)
    DeviceID: str = Field(description="设备编码", max_length=20)
    LeftTopX: int | None = Field(description="左上角X坐标")
    LeftTopY: int | None = Field(description="左上角Y坐标")
    RightBtmX: int | None = Field(description="右下角X坐标")
    RightBtmY: int | None = Field(description="右下角Y坐标")

    SubImageList: SubImageInfoList | None = Field(
        default=None, description="图像列表", sa_column=Column(JSON)
    )


class FaceList(SQLModel):
    """GA/T 1400.3-2017 C.9 人脸对象列表"""

    FaceObject: list[Face]


# 人脸对象列表结构
class FaceListObjectSchema(SQLModel):
    FaceListObject: FaceList


class FaceQueryParams(SQLModel):
    """GA/T 1400.4 `/VIID/Faces` 查询字符串中的分页条件。"""

    RecordStartNo: int = Field(default=0, ge=0, description="起始记录号")
    PageRecordNum: int | None = Field(default=None, ge=1, description="本页记录数")
