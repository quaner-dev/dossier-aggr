from sqlalchemy import JSON, Column, UniqueConstraint
from sqlmodel import Field

from domain.archive.archive_subject import (
    ArchiveSubject as ArchiveSubjectDomain,
)
from schemas import (
    FaceList,
    GaitList,
    MotorVehicleList,
    NonMotorVehicleList,
    PersonList,
)


class ArchiveSubject(ArchiveSubjectDomain, table=True):
    __table_args__ = (UniqueConstraint("ArchiveID"),)

    id: int | None = Field(default=None, primary_key=True, exclude=True)
    PersonIDList: list[str] | None = Field(default=None, sa_column=Column(JSON))
    FaceIDList: list[str] | None = Field(default=None, sa_column=Column(JSON))
    GaitIDList: list[str] | None = Field(default=None, sa_column=Column(JSON))
    MotorVehicleIDList: list[str] | None = Field(default=None, sa_column=Column(JSON))
    NonMotorVehicleIDList: list[str] | None = Field(default=None, sa_column=Column(JSON))
    PersonObjectList: PersonList | None = Field(default=None, sa_column=Column(JSON))
    FaceObjectList: FaceList | None = Field(default=None, sa_column=Column(JSON))
    GaitObjectList: GaitList | None = Field(default=None, sa_column=Column(JSON))
    MotorVehicleObjectList: MotorVehicleList | None = Field(default=None, sa_column=Column(JSON))
    NonMotorVehicleObjectList: NonMotorVehicleList | None = Field(default=None, sa_column=Column(JSON))
