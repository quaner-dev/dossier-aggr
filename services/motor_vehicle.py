from typing import List

from sqlmodel import select

from schemas import MotorVehicle
import tasks
from models import MotorVehicle as MotorVehicleModel
from base import MotorVehicleBase
import exceptions
from .common import BaseService


class MotorVehicleService(BaseService):
    async def create_motor_vehicle(self, motor_vehicle: MotorVehicle):
        await tasks.create_motor_vehicle.kiq(motor_vehicle)

    async def batch_create_motor_vehicles(
        self, motor_vehicles: List[MotorVehicle]
    ):
        for motor_vehicle in motor_vehicles:
            await tasks.create_motor_vehicle.kiq(motor_vehicle)

    async def get_motor_vehicle(self, motor_vehicle_id: str) -> MotorVehicleBase:
        """根据MotorVehicleID查询机动车信息"""
        statement = select(MotorVehicleModel).where(MotorVehicleModel.MotorVehicleID == motor_vehicle_id)
        motor_vehicle = (await self.session.exec(statement)).first()
        if not motor_vehicle:
            raise exceptions.DataNotFoundError(detail=f"{motor_vehicle_id} not exist")
        return MotorVehicleBase.model_validate(motor_vehicle)

    async def list_motor_vehicles(self) -> List[MotorVehicleBase]:
        """查询所有机动车信息"""
        statement = select(MotorVehicleModel)
        motor_vehicles = (await self.session.exec(statement)).all()
        if not motor_vehicles:
            raise exceptions.DataNotFoundError(detail="No MotorVehicle data exist")
        return [MotorVehicleBase.model_validate(mv) for mv in motor_vehicles]

    async def update_motor_vehicle(self, motor_vehicle_id: str, motor_vehicle: MotorVehicle) -> MotorVehicleModel:
        """更新机动车信息"""
        statement = select(MotorVehicleModel).where(MotorVehicleModel.MotorVehicleID == motor_vehicle_id)
        db_mv = (await self.session.exec(statement)).first()
        if not db_mv:
            raise exceptions.DataNotFoundError(detail=f"{motor_vehicle_id} not exist")
        
        mv_base = MotorVehicleBase.model_validate(motor_vehicle)
        for key, value in mv_base.model_dump(exclude={"id"}).items():
            setattr(db_mv, key, value)
        
        self.session.add(db_mv)
        await self.session.commit()
        await self.session.refresh(db_mv)
        return db_mv

    async def delete_motor_vehicle(self, motor_vehicle_id: str) -> None:
        """删除机动车信息"""
        statement = select(MotorVehicleModel).where(MotorVehicleModel.MotorVehicleID == motor_vehicle_id)
        db_mv = (await self.session.exec(statement)).first()
        if not db_mv:
            raise exceptions.DataNotFoundError(detail=f"{motor_vehicle_id} not exist")
        
        await self.session.delete(db_mv)
        await self.session.commit()
