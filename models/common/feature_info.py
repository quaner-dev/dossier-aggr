from sqlmodel import SQLModel, Field


class FeatureInfo(SQLModel):
    """视图库对接技术要求 A.7 特征值对象"""

    id: int | None = Field(default=None, primary_key=True, exclude=True)
    sub_image_info_id: str | None = Field(
        default=None, foreign_key="subimageinfo.ImageID", unique=True, exclude=True
    )

    Vendor: str = Field(description="厂商", max_length=100)
    AlgorithmVersion: str = Field(description="算法版本", max_length=100)
    FeatureData: str = Field(description="特征值数据")
