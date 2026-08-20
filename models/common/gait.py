from sqlmodel import Field, SQLModel

from . import enums
from .sub_image_info import SubImageInfoList


class Gait(SQLModel):
    """GA/T 2350.5-2025 B.16 步态对象"""

    GaitID: str = Field(description="步态标识", max_length=48)
    SourceID: str = Field(description="来源标识", max_length=41)
    Angle: int | None = Field(default=None, description="角度")
    GaitAppearTime: enums.VIIDDateTime | None = Field(
        default=None, description="步态出现时间"
    )
    GaitDisappearTime: enums.VIIDDateTime | None = Field(
        default=None, description="步态消失时间"
    )
    Similaritydegree: float | None = Field(default=None, description="相似度")
    InfoKind: enums.InfoKindEnum = Field(description="信息分类")
    GenderCode: enums.GenderTypeEnum | None = Field(default=None, description="性别代码")
    AgeUpLimit: int | None = Field(default=None, description="年龄上限")
    AgeLowerLimit: int | None = Field(default=None, description="年龄下限")
    AccompanyNumber: int | None = Field(default=None, description="同行人数")
    HeightUpLimit: int | None = Field(default=None, description="身高上限")
    HeightLowerLimit: int | None = Field(default=None, description="身高下限")
    SubImageList: SubImageInfoList | None = Field(default=None, description="图片列表")


class GaitList(SQLModel):
    """GA/T 2350.5-2025 B.16 步态对象列表"""

    GaitObject: list[Gait]
