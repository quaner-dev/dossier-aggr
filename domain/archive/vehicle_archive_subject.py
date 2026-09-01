from sqlmodel import Field, SQLModel


class VehicleArchiveSubject(SQLModel):
    """GA/T 2350.5-2025 B.5 车辆档案明细对象"""

    ArchiveID: str = Field(max_length=48, description="档案标识")
