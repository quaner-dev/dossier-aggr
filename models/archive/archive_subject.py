from typing import Any

from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field

from ..common.gait import GaitList
from ..person.person import PersonList
from ..face.face import FaceList


class MotorVehicleList(SQLModel):
    MotorVehicleObject: list[dict[str, Any]]


class NonMotorVehicleList(SQLModel):
    NonMotorVehicleObject: list[dict[str, Any]]


class ArchiveSubject(SQLModel, table=True):
    """GA/T 2350.5-2025 B.5 档案明细信息对象"""

    id: int | None = Field(default=None, primary_key=True, exclude=True)

    ArchiveID: str = Field(max_length=48, description="档案标识", unique=True)
    PersonIDList: list[str] | None = Field(
        default=None,
        description="人员信息标识列表",
        sa_column=Column(JSON),
    )
    FaceIDList: list[str] | None = Field(
        default=None,
        description="人脸信息标识列表",
        sa_column=Column(JSON),
    )
    GaitIDList: list[str] | None = Field(
        default=None,
        description="步态信息标识列表",
        sa_column=Column(JSON),
    )
    MotorVehicleIDList: list[str] | None = Field(
        default=None,
        description="机动车信息标识列表",
        sa_column=Column(JSON),
    )
    NonMotorVehicleIDList: list[str] | None = Field(
        default=None,
        description="非机动车信息标识列表",
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


# 档案明细列表
class ArchiveSubjectList(SQLModel):
    ArchiveSubjectObject: list[ArchiveSubject]


# 档案明细列表结构
class ArchiveSubjectSchema(SQLModel):
    ArchiveSubjectListObject: ArchiveSubjectList
