from typing import List

from sqlmodel import select

from schemas import NonMotorVehicle
import tasks
from models import NonMotorVehicle as NonMotorVehicleModel
from base import NonMotorVehicleBase
import exceptions
from .common import BaseService


class NonMotorVehicleService(BaseService):
    async def create_non_motor_vehicle(self, non_motor_vehicle: NonMotorVehicle):
        await tasks.create_non_motor_vehicle.kiq(non_motor_vehicle)

    async def batch_create_non_motor_vehicles(
        self, non_motor_vehicles: List[NonMotorVehicle]
    ):
        for non_motor_vehicle in non_motor_vehicles:
            await tasks.create_non_motor_vehicle.kiq(non_motor_vehicle)

    async def get_non_motor_vehicle(self, non_motor_vehicle_id: str) -> NonMotorVehicleBase:
        """根据NonMotorVehicleID查询非机动车信息"""
        statement = select(NonMotorVehicleModel).where(NonMotorVehicleModel.NonMotorVehicleID == non_motor_vehicle_id)
        non_motor_vehicle = (await self.session.exec(statement)).first()
        if not non_motor_vehicle:
            raise exceptions.DataNotFoundError(detail=f"{non_motor_vehicle_id} not exist")
        return NonMotorVehicleBase.model_validate(non_motor_vehicle)

    async def list_non_motor_vehicles(self) -> List[NonMotorVehicleBase]:
        """查询所有非机动车信息"""
        statement = select(NonMotorVehicleModel)
        non_motor_vehicles = (await self.session.exec(statement)).all()
        if not non_motor_vehicles:
            raise exceptions.DataNotFoundError(detail="No NonMotorVehicle data exist")
        return [NonMotorVehicleBase.model_validate(nmv) for nmv in non_motor_vehicles]

    async def update_non_motor_vehicle(self, non_motor_vehicle_id: str, non_motor_vehicle: NonMotorVehicle) -> NonMotorVehicleModel:
        """更新非机动车信息"""
        statement = select(NonMotorVehicleModel).where(NonMotorVehicleModel.NonMotorVehicleID == non_motor_vehicle_id)
        db_nmv = (await self.session.exec(statement)).first()
        if not db_nmv:
            raise exceptions.DataNotFoundError(detail=f"{non_motor_vehicle_id} not exist")
        
        nmv_base = NonMotorVehicleBase.model_validate(non_motor_vehicle)
        for key, value in nmv_base.model_dump(exclude={"id"}).items():
            setattr(db_nmv, key, value)
        
        self.session.add(db_nmv)
        await self.session.commit()
        await self.session.refresh(db_nmv)
        return db_nmv

    async def delete_non_motor_vehicle(self, non_motor_vehicle_id: str) -> None:
        """删除非机动车信息"""
        statement = select(NonMotorVehicleModel).where(NonMotorVehicleModel.NonMotorVehicleID == non_motor_vehicle_id)
        db_nmv = (await self.session.exec(statement)).first()
        if not db_nmv:
            raise exceptions.DataNotFoundError(detail=f"{non_motor_vehicle_id} not exist")
        
        await self.session.delete(db_nmv)
        await self.session.commit()
