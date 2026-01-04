from datetime import datetime

from fastapi import APIRouter

import tasks
import schemas
import constants

router = APIRouter()


@router.post(
    path=constants.PERSONS_URL,
    response_model=schemas.ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.11.1 批量人员增加",
)
async def persons_create(data: schemas.PersonListObjectSchema):
    """批量人员增加接口"""
    # TODO 先编写face模块的逻辑，再编写face的逻辑就可以了
    persons = data.PersonListObject.PersonObject
    for person in persons:
        await tasks.create_person.kiq(person)

    response_status_objects = [
        schemas.ResponseStatus(
            RequestURL=constants.PERSONS_URL,
            StatusCode="0",
            StatusString="上传成功",
            Id=person.PersonID,
            LocalTime=datetime.now(),
        )
        for person in persons
    ]

    return schemas.ResponseStatusListSchema(
        ResponseStatusListObject=schemas.ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )
