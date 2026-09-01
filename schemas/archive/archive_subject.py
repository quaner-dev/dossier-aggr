from typing import Any

from sqlmodel import Field, SQLModel

from domain.archive import ArchiveSubject as ArchiveSubjectDomain

from ..common import GaitList
from ..face import FaceList
from ..person import PersonList


class MotorVehicleList(SQLModel):
    MotorVehicleObject: list[dict[str, Any]]


class NonMotorVehicleList(SQLModel):
    NonMotorVehicleObject: list[dict[str, Any]]


class ArchiveSubject(ArchiveSubjectDomain):
    PersonIDList: list[str] | None = Field(default=None, description="人员信息标识列表")
    FaceIDList: list[str] | None = Field(default=None, description="人脸信息标识列表")
    GaitIDList: list[str] | None = Field(default=None, description="步态信息标识列表")
    MotorVehicleIDList: list[str] | None = Field(
        default=None, description="机动车信息标识列表"
    )
    NonMotorVehicleIDList: list[str] | None = Field(
        default=None, description="非机动车信息标识列表"
    )
    PersonObjectList: PersonList | None = Field(default=None, description="人员完整信息列表")
    FaceObjectList: FaceList | None = Field(default=None, description="人脸完整信息列表")
    GaitObjectList: GaitList | None = Field(default=None, description="步态完整信息列表")
    MotorVehicleObjectList: MotorVehicleList | None = Field(
        default=None, description="机动车完整信息列表"
    )
    NonMotorVehicleObjectList: NonMotorVehicleList | None = Field(
        default=None, description="非机动车完整信息列表"
    )


class ArchiveSubjectList(SQLModel):
    ArchiveSubjectObject: list[ArchiveSubject]


class ArchiveSubjectSchema(SQLModel):
    ArchiveSubjectListObject: ArchiveSubjectList
