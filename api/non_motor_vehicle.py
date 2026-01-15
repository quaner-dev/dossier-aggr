from datetime import datetime

from fastapi import APIRouter, Depends, Query

from schemas import (
    ResponseStatusListSchema,
    NonMotorVehicleListObjectSchema,
    NonMotorVehicleList,
    ResponseStatus,
    ResponseStatusList,
)
import constants
from services import NonMotorVehicleService

router = APIRouter()


@router.get(
    path=constants.NON_MOTOR_VEHICLES_URL,
    response_model=NonMotorVehicleListObjectSchema,
    description="GA/T 1400.4-2017 7.2.13.4 非机动车查询",
)
async def non_motor_vehicles_query(
    non_motor_vehicle_id: str | None = Query(None, alias="NonMotorVehicleID", max_length=33),
    service: NonMotorVehicleService = Depends(NonMotorVehicleService),
):
    """非机动车查询接口"""
    if non_motor_vehicle_id:
        non_motor_vehicle = await service.get_non_motor_vehicle(non_motor_vehicle_id)
        return NonMotorVehicleListObjectSchema(
            NonMotorVehicleListObject=NonMotorVehicleList(NonMotorVehicleObject=[non_motor_vehicle])
        )
    else:
        non_motor_vehicles = await service.list_non_motor_vehicles()
        return NonMotorVehicleListObjectSchema(
            NonMotorVehicleListObject=NonMotorVehicleList(NonMotorVehicleObject=non_motor_vehicles)
        )


@router.post(
    path=constants.NON_MOTOR_VEHICLES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.13.1 批量非机动车增加",
)
async def non_motor_vehicles_create(
    data: NonMotorVehicleListObjectSchema,
    service: NonMotorVehicleService = Depends(NonMotorVehicleService),
):
    """批量非机动车增加接口"""
    non_motor_vehicles = data.NonMotorVehicleListObject.NonMotorVehicleObject
    await service.batch_create_non_motor_vehicles(non_motor_vehicles)

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.NON_MOTOR_VEHICLES_URL,
            StatusCode="0",
            StatusString="上传成功",
            Id=non_motor_vehicle.NonMotorVehicleID,
            LocalTime=datetime.now(),
        )
        for non_motor_vehicle in non_motor_vehicles
    ]

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )


@router.put(
    path=constants.NON_MOTOR_VEHICLES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.13.2 批量非机动车修改",
)
async def non_motor_vehicles_update(
    data: NonMotorVehicleListObjectSchema,
    service: NonMotorVehicleService = Depends(NonMotorVehicleService),
):
    """批量非机动车修改接口"""
    non_motor_vehicles = data.NonMotorVehicleListObject.NonMotorVehicleObject
    for non_motor_vehicle in non_motor_vehicles:
        await service.update_non_motor_vehicle(non_motor_vehicle.NonMotorVehicleID, non_motor_vehicle)

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.NON_MOTOR_VEHICLES_URL,
            StatusCode="0",
            StatusString="修改成功",
            Id=non_motor_vehicle.NonMotorVehicleID,
            LocalTime=datetime.now(),
        )
        for non_motor_vehicle in non_motor_vehicles
    ]

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )


@router.delete(
    path=constants.NON_MOTOR_VEHICLES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.13.3 批量非机动车删除",
)
async def non_motor_vehicles_delete(
    id_list: str = Query(..., alias="IDList"),
    service: NonMotorVehicleService = Depends(NonMotorVehicleService),
):
    """批量非机动车删除接口"""
    non_motor_vehicle_ids = [id.strip() for id in id_list.split(",")]
    
    for non_motor_vehicle_id in non_motor_vehicle_ids:
        await service.delete_non_motor_vehicle(non_motor_vehicle_id)

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.NON_MOTOR_VEHICLES_URL,
            StatusCode="0",
            StatusString="删除成功",
            Id=non_motor_vehicle_id,
            LocalTime=datetime.now(),
        )
        for non_motor_vehicle_id in non_motor_vehicle_ids
    ]

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )
