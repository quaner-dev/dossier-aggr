from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel

from . import enums
from .feature_info import FeatureInfo


class SubImageInfo(SQLModel):
    """GA/T 1400.3-2017 C.6 图像子对象"""

    ImageID: str | None = Field(default=None, description="图像标识", max_length=41)
    InfoKind: enums.InfoKindEnum = Field(
        default=enums.InfoKindEnum.Other, description="信息分类"
    )
    ImageSource: str = Field(description="图像来源", max_length=2)
    EventSort: int | None = Field(default=None, description="事件分类")
    DeviceID: str | None = Field(default=None, description="设备编码", max_length=20)
    StoragePath: str | None = Field(
        default=None, description="存储路径", max_length=256
    )
    Type: enums.ImageTypeEnum = Field(description="图片类型")
    FileFormat: enums.ImageFormatEnum = Field(description="图像文件格式")
    ShotTime: str | None = Field(default=None, description="拍摄时间")
    Width: int | None = Field(description="水平像素值")
    Height: int | None = Field(description="垂直像素值")
    Data: str | None = Field(description="图像数据")

    FeatureInfoObject: FeatureInfo = Field(
        description="特征值属性", sa_column=Column(JSON)
    )
