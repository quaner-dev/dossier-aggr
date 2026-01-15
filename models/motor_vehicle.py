from sqlmodel import Field, SQLModel  # type: ignore

import base


class MotorVehicleSubImageInfoLink(SQLModel, table=True):
    MotorVehicleID: str = Field(
        foreign_key="motorvehicle.MotorVehicleID", primary_key=True
    )
    ImageID: str = Field(
        foreign_key="subimageinfo.ImageID", primary_key=True, unique=True
    )


class MotorVehicle(base.motor_vehicle.MotorVehicleBase, table=True): ...
