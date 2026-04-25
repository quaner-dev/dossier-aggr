from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field

from .archive_subject import MotorVehicleList, NonMotorVehicleList
from ..common.gait import GaitList
from ..face.face import FaceList
from ..person.person import PersonList


class VehicleArchiveSubject(SQLModel, table=True):
    """GA/T 2350.5-2025 车辆档案明细对象"""

    id: int | None = Field(default=None, primary_key=True, exclude=True)

    ArchiveID: str = Field(max_length=48, description="档案标识", unique=True)
    MotorVehicleIDList: list[str] | None = Field(
        default=None,
        description="机动车标识列表",
        sa_column=Column(JSON),
    )
    PersonIDList: list[str] | None = Field(
        default=None,
        description="人员标识列表",
        sa_column=Column(JSON),
    )
    FaceIDList: list[str] | None = Field(
        default=None,
        description="人脸标识列表",
        sa_column=Column(JSON),
    )
    GaitIDList: list[str] | None = Field(
        default=None,
        description="步态标识列表",
        sa_column=Column(JSON),
    )
    NonMotorVehicleIDList: list[str] | None = Field(
        default=None,
        description="非机动车标识列表",
        sa_column=Column(JSON),
    )
    PersonObjectList: PersonList | None = Field(
        default=None,
        description="人员完整信息列表",
        sa_column=Column(JSON),
    )
    FaceObjectList: FaceList | None = Field(
        default=None,
        description="人脸完整信息列表",
        sa_column=Column(JSON),
    )
    GaitObjectList: GaitList | None = Field(
        default=None,
        description="步态完整信息列表",
        sa_column=Column(JSON),
    )
    MotorVehicleObjectList: MotorVehicleList | None = Field(
        default=None,
        description="机动车完整信息列表",
        sa_column=Column(JSON),
    )
    NonMotorVehicleObjectList: NonMotorVehicleList | None = Field(
        default=None,
        description="非机动车完整信息列表",
        sa_column=Column(JSON),
    )


class VehicleArchiveSubjectList(SQLModel):
    VehicleArchiveSubjectObject: list[VehicleArchiveSubject]


class VehicleArchiveSubjectSchema(SQLModel):
    VehicleArchiveSubjectListObject: VehicleArchiveSubjectList
