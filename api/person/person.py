from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from core import constants, exceptions
from core.time import CHINA_TZ
from core.utils import parse_id_list
from schemas import (
    Person,
    PersonList,
    PersonListObjectSchema,
    ResponseStatus,
    ResponseStatusList,
    ResponseStatusListSchema,
)
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
        PersonListObject=PersonList(
            PersonObject=[
                Person.model_validate(person, from_attributes=True) for person in persons
            ]
        )
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
                    StatusString="已接收",
                    Id=person.PersonID,
                    LocalTime=datetime.now(tz=CHINA_TZ),
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
    await service.update_persons(persons=persons)

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.PERSONS_URL,
                    StatusCode="0",
                    StatusString="修改成功",
                    Id=person.PersonID,
                    LocalTime=datetime.now(tz=CHINA_TZ),
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
    person_ids: Annotated[
        str | list[str] | None,
        Query(alias="IDList"),
    ] = None,
    legacy_person_ids: Annotated[
        str | list[str] | None,
        Query(alias="person_ids", include_in_schema=False),
    ] = None,
) -> ResponseStatusListSchema:
    """批量人员删除接口"""
    raw_person_ids = person_ids if person_ids is not None else legacy_person_ids
    if raw_person_ids is None:
        raise exceptions.InvalidParameterError(detail="IDList is required")

    parsed_person_ids = parse_id_list(raw_person_ids)
    await service.delete_persons(person_ids=parsed_person_ids)

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=constants.PERSONS_URL,
                    StatusCode="0",
                    StatusString="删除成功",
                    Id=person_id,
                    LocalTime=datetime.now(tz=CHINA_TZ),
                )
                for person_id in parsed_person_ids
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
    return Person.model_validate(person, from_attributes=True)


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
    await service.update_person(data)
    return ResponseStatus(
        RequestURL=f"{constants.PERSONS_URL}/{person_id}",
        StatusCode="0",
        StatusString="修改成功",
        Id=person_id,
        LocalTime=datetime.now(tz=CHINA_TZ),
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
    await service.delete_person(person_id)
    return ResponseStatus(
        RequestURL=f"{constants.PERSONS_URL}/{person_id}",
        StatusCode="0",
        StatusString="删除成功",
        Id=person_id,
        LocalTime=datetime.now(tz=CHINA_TZ),
    )
