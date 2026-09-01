from sqlmodel import Field, SQLModel

from domain.archive import VehicleArchiveSubject as VehicleArchiveSubjectDomain

from ..common import GaitList
from ..face import FaceList
from ..person import PersonList
from .archive_subject import MotorVehicleList, NonMotorVehicleList


class VehicleArchiveSubject(VehicleArchiveSubjectDomain):
    MotorVehicleIDList: list[str] | None = Field(default=None, description="机动车标识列表")
    PersonIDList: list[str] | None = Field(default=None, description="人员标识列表")
    FaceIDList: list[str] | None = Field(default=None, description="人脸标识列表")
    GaitIDList: list[str] | None = Field(default=None, description="步态标识列表")
    NonMotorVehicleIDList: list[str] | None = Field(
        default=None, description="非机动车标识列表"
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


class VehicleArchiveSubjectList(SQLModel):
    VehicleArchiveSubjectObject: list[VehicleArchiveSubject]


class VehicleArchiveSubjectSchema(SQLModel):
    VehicleArchiveSubjectListObject: VehicleArchiveSubjectList
