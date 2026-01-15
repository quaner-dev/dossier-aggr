from sqlmodel import Field, SQLModel  # type: ignore

import base


class NonMotorVehicleSubImageInfoLink(SQLModel, table=True):
    NonMotorVehicleID: str = Field(
        foreign_key="nonmotorvehicle.NonMotorVehicleID", primary_key=True
    )
    ImageID: str = Field(
        foreign_key="subimageinfo.ImageID", primary_key=True, unique=True
    )


class NonMotorVehicle(base.non_motor_vehicle.NonMotorVehicleBase, table=True): ...
