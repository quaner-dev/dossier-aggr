from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field


class VehicleArchiveSubject(SQLModel, table=True):
    """GA/T 2350.5-2025 车辆档案明细对象"""

    id: int | None = Field(default=None, primary_key=True, exclude=True)

    ArchiveID: str = Field(max_length=48, description="档案标识", unique=True)
    MotorVehicleIDList: list[str] | None = Field(
        default=None,
        description="机动车标识列表",
        sa_column=Column(JSON),
    )
    NonMotorVehicleIDList: list[str] | None = Field(
        default=None,
        description="非机动车标识列表",
        sa_column=Column(JSON),
    )
    ImageID: str | None = Field(default=None, description="图像标识", max_length=41)


class VehicleArchiveSubjectList(SQLModel):
    VehicleArchiveSubjectObject: list[VehicleArchiveSubject]


class VehicleArchiveSubjectSchema(SQLModel):
    VehicleArchiveSubjectListObject: VehicleArchiveSubjectList
