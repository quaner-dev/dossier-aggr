from datetime import datetime

from fastapi import APIRouter, Depends, Query

from schemas import (
    ResponseStatusListSchema,
    MotorVehicleListObjectSchema,
    MotorVehicleList,
    ResponseStatus,
    ResponseStatusList,
)
import constants
from services import MotorVehicleService

router = APIRouter()


@router.get(
    path=constants.MOTOR_VEHICLES_URL,
    response_model=MotorVehicleListObjectSchema,
    description="GA/T 1400.4-2017 7.2.14.4 机动车查询",
)
async def motor_vehicles_query(
    motor_vehicle_id: str | None = Query(None, alias="MotorVehicleID", max_length=33),
    service: MotorVehicleService = Depends(MotorVehicleService),
):
    """机动车查询接口"""
    if motor_vehicle_id:
        motor_vehicle = await service.get_motor_vehicle(motor_vehicle_id)
        return MotorVehicleListObjectSchema(
            MotorVehicleListObject=MotorVehicleList(MotorVehicleObject=[motor_vehicle])
        )
    else:
        motor_vehicles = await service.list_motor_vehicles()
        return MotorVehicleListObjectSchema(
            MotorVehicleListObject=MotorVehicleList(MotorVehicleObject=motor_vehicles)
        )


@router.post(
    path=constants.MOTOR_VEHICLES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.14.1 批量机动车增加",
)
async def motor_vehicles_create(
    data: MotorVehicleListObjectSchema,
    service: MotorVehicleService = Depends(MotorVehicleService),
):
    """批量机动车增加接口"""
    motor_vehicles = data.MotorVehicleListObject.MotorVehicleObject
    await service.batch_create_motor_vehicles(motor_vehicles)

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.MOTOR_VEHICLES_URL,
            StatusCode="0",
            StatusString="上传成功",
            Id=motor_vehicle.MotorVehicleID,
            LocalTime=datetime.now(),
        )
        for motor_vehicle in motor_vehicles
    ]

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )


@router.put(
    path=constants.MOTOR_VEHICLES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.14.2 批量机动车修改",
)
async def motor_vehicles_update(
    data: MotorVehicleListObjectSchema,
    service: MotorVehicleService = Depends(MotorVehicleService),
):
    """批量机动车修改接口"""
    motor_vehicles = data.MotorVehicleListObject.MotorVehicleObject
    for motor_vehicle in motor_vehicles:
        await service.update_motor_vehicle(motor_vehicle.MotorVehicleID, motor_vehicle)

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.MOTOR_VEHICLES_URL,
            StatusCode="0",
            StatusString="修改成功",
            Id=motor_vehicle.MotorVehicleID,
            LocalTime=datetime.now(),
        )
        for motor_vehicle in motor_vehicles
    ]

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )


@router.delete(
    path=constants.MOTOR_VEHICLES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.14.3 批量机动车删除",
)
async def motor_vehicles_delete(
    id_list: str = Query(..., alias="IDList"),
    service: MotorVehicleService = Depends(MotorVehicleService),
):
    """批量机动车删除接口"""
    motor_vehicle_ids = [id.strip() for id in id_list.split(",")]
    
    for motor_vehicle_id in motor_vehicle_ids:
        await service.delete_motor_vehicle(motor_vehicle_id)

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.MOTOR_VEHICLES_URL,
            StatusCode="0",
            StatusString="删除成功",
            Id=motor_vehicle_id,
            LocalTime=datetime.now(),
        )
        for motor_vehicle_id in motor_vehicle_ids
    ]

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )
