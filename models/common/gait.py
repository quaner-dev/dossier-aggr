from sqlmodel import SQLModel, Field


class Gait(SQLModel):
    """GA/T 2350.5-2025 B.16 步态对象"""

    Vendor: str | None = Field(default=None, description="算法厂商", max_length=100)
    AlgorithmVersion: str | None = Field(
        default=None, description="算法版本", max_length=100
    )
    GaitData: str | None = Field(default=None, description="步态特征数据")
