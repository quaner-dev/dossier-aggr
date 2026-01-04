from sqlmodel import Field, SQLModel  # type: ignore

import base.enums as enums


class PersonBase(SQLModel):
    """GA/T 1400.3-2017 A.8 人员对象"""

    id: int | None = Field(default=None, primary_key=True, exclude=True)

    PersonID: str = Field(description="人员标识", max_length=33, unique=True)
    InfoKind: enums.InfoKindEnum = Field(
        default=enums.InfoKindEnum.Other, description="信息分类"
    )
    SourceID: str = Field(description="来源标识", max_length=41)
    DeviceID: str = Field(description="设备编码", max_length=20)
    LeftTopX: int | None = Field(description="左上角X坐标")
    LeftTopY: int | None = Field(description="左上角Y坐标")
    RightBtmX: int | None = Field(description="右下角X坐标")
    RightBtmY: int | None = Field(description="右下角Y坐标")
