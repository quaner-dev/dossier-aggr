from datetime import datetime

from fastapi import APIRouter, Depends, Query

import tasks
from schemas import (
    ResponseStatusListSchema,
    PersonListObjectSchema,
    PersonList,
    ResponseStatus,
    ResponseStatusList,
)
import constants
from services import PersonService

router = APIRouter()


@router.get(
    path=constants.PERSONS_URL,
    response_model=PersonListObjectSchema,
    description="GA/T 1400.4-2017 7.2.11.4 人员查询",
)
async def persons_query(
    person_id: str | None = Query(None, alias="PersonID", max_length=33),
    service: PersonService = Depends(PersonService),
):
    """人员查询接口"""
    if person_id:
        person = await service.get_person(person_id)
        return PersonListObjectSchema(PersonListObject=PersonList(PersonObject=[person]))
    else:
        persons = await service.list_persons()
        return PersonListObjectSchema(PersonListObject=PersonList(PersonObject=persons))


@router.post(
    path=constants.PERSONS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.11.1 批量人员增加",
)
async def persons_create(data: PersonListObjectSchema):
    """批量人员增加接口"""
    # TODO 先编写face模块的逻辑，再编写face的逻辑就可以了
    persons = data.PersonListObject.PersonObject
    for person in persons:
        await tasks.create_person.kiq(person)

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.PERSONS_URL,
            StatusCode="0",
            StatusString="上传成功",
            Id=person.PersonID,
            LocalTime=datetime.now(),
        )
        for person in persons
    ]

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )


@router.put(
    path=constants.PERSONS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.11.2 批量人员修改",
)
async def persons_update(
    data: PersonListObjectSchema,
    service: PersonService = Depends(PersonService),
):
    """批量人员修改接口"""
    persons = data.PersonListObject.PersonObject
    for person in persons:
        await service.update_person(person.PersonID, person)

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.PERSONS_URL,
            StatusCode="0",
            StatusString="修改成功",
            Id=person.PersonID,
            LocalTime=datetime.now(),
        )
        for person in persons
    ]

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )


@router.delete(
    path=constants.PERSONS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.11.3 批量人员删除",
)
async def persons_delete(
    id_list: str = Query(..., alias="IDList"),
    service: PersonService = Depends(PersonService),
):
    """批量人员删除接口"""
    person_ids = [id.strip() for id in id_list.split(",")]
    
    for person_id in person_ids:
        await service.delete_person(person_id)

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.PERSONS_URL,
            StatusCode="0",
            StatusString="删除成功",
            Id=person_id,
            LocalTime=datetime.now(),
        )
        for person_id in person_ids
    ]

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )
