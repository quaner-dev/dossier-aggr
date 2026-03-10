from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BeforeValidator

from models import (
    ResponseStatusListSchema,
    PersonListObjectSchema,
    Person,
    PersonList,
    ResponseStatus,
    ResponseStatusList,
)
from core import constants
from core.utils import parse_id_list
from services import PersonService

router = APIRouter()


@router.get(
    path=constants.PERSONS_URL,
    response_model=PersonListObjectSchema,
    description="GA/T 1400.4-2017 7.2.11.1 批量人员的查询",
)
async def persons_query(
    service: Annotated[PersonService, Depends(PersonService)],
) -> PersonListObjectSchema:
    """批量人员查询接口"""
    persons = await service.list_persons()

    return PersonListObjectSchema(
        PersonListObject=PersonList(PersonObject=[person for person in persons])
    )


@router.post(
    path=constants.PERSONS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.11.1 批量人员的增加",
)
async def persons_create(
    data: PersonListObjectSchema,
    service: Annotated[PersonService, Depends(PersonService)],
) -> ResponseStatusListSchema:
    """批量人员增加接口"""
    persons = data.PersonListObject.PersonObject
    _ = await service.create_persons(persons=persons)

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.PERSONS_URL,
                    StatusCode="0",
                    StatusString="上传成功",
                    Id=person.PersonID,
                    LocalTime=datetime.now(),
                )
                for person in persons
            ]
        )
    )


@router.put(
    path=constants.PERSONS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.11.1 批量人员的修改",
)
async def persons_update(
    data: PersonListObjectSchema,
    service: Annotated[PersonService, Depends(PersonService)],
) -> ResponseStatusListSchema:
    """批量人员修改接口"""
    persons = data.PersonListObject.PersonObject
    _ = await service.update_persons(persons=persons)

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.PERSONS_URL,
                    StatusCode="0",
                    StatusString="修改成功",
                    Id=person.PersonID,
                    LocalTime=datetime.now(),
                )
                for person in persons
            ]
        )
    )


@router.delete(
    path=constants.PERSONS_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.11.1 批量人员的删除",
)
async def persons_delete(
    service: Annotated[PersonService, Depends(PersonService)],
    person_ids: Annotated[list[str], BeforeValidator(parse_id_list)],
) -> ResponseStatusListSchema:
    """批量人员删除接口"""
    _ = await service.delete_persons(person_ids=person_ids)

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.PERSONS_URL,
                    StatusCode="0",
                    StatusString="删除成功",
                    Id=person_id,
                    LocalTime=datetime.now(),
                )
                for person_id in person_ids
            ]
        )
    )


@router.get(
    path=f"{constants.PERSONS_URL}/{{person_id}}",
    response_model=Person,
    description="GA/T 1400.4-2017 7.2.11.2 单个人员的查询",
)
async def person_query(
    person_id: str,
    service: Annotated[PersonService, Depends(PersonService)],
) -> Person:
    """单个人员查询接口"""
    person = await service.get_person(person_id)
    return person


@router.put(
    path=f"{constants.PERSONS_URL}/{{person_id}}",
    response_model=ResponseStatus,
    description="GA/T 1400.4-2017 7.2.11.2 单个人员的修改",
)
async def person_update(
    person_id: str,
    data: Person,
    service: Annotated[PersonService, Depends(PersonService)],
) -> ResponseStatus:
    """单个人员修改接口"""
    data.PersonID = person_id
    _ = await service.update_person(data)
    return ResponseStatus(
        RequestURL=f"{constants.PERSONS_URL}/{person_id}",
        StatusCode="0",
        StatusString="修改成功",
        Id=person_id,
        LocalTime=datetime.now(),
    )


@router.delete(
    path=f"{constants.PERSONS_URL}/{{person_id}}",
    response_model=ResponseStatus,
    description="GA/T 1400.4-2017 7.2.11.2 单个人员的删除",
)
async def person_delete(
    person_id: str,
    service: Annotated[PersonService, Depends(PersonService)],
) -> ResponseStatus:
    """单个人员删除接口"""
    _ = await service.delete_person(person_id)
    return ResponseStatus(
        RequestURL=f"{constants.PERSONS_URL}/{person_id}",
        StatusCode="0",
        StatusString="删除成功",
        Id=person_id,
        LocalTime=datetime.now(),
    )
