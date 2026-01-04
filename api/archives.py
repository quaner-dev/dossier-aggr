from datetime import datetime

from fastapi import APIRouter

import schemas
import constants

router = APIRouter()


@router.post(
    path=constants.ARCHIVES_URL,
    response_model=schemas.ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.10 人员档案增加接口",
)
async def archives_create(data: schemas.ArchiveListSchema):
    archives = data.ArchiveListObject.ArchiveObject

    response_status_objects = [
        schemas.ResponseStatus(
            RequestURL=constants.SUBSCRIBE_NOTIFICATIONS_URL,
            StatusCode="0",
            StatusString="档案创建成功",
            Id=archive.ArchiveID,
            LocalTime=datetime.now(),
        )
        for archive in archives
    ]
    return schemas.ResponseStatusListSchema(
        ResponseStatusListObject=schemas.ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )


@router.put(
    path=constants.ARCHIVES_URL,
    response_model=schemas.ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.10 人员档案更新接口",
)
async def archives_update(data: schemas.ArchiveListSchema):
    archives = data.ArchiveListObject.ArchiveObject

    response_status_objects = [
        schemas.ResponseStatus(
            RequestURL=constants.SUBSCRIBE_NOTIFICATIONS_URL,
            StatusCode="0",
            StatusString="档案更新成功",
            Id=archive.ArchiveID,
            LocalTime=datetime.now(),
        )
        for archive in archives
    ]
    return schemas.ResponseStatusListSchema(
        ResponseStatusListObject=schemas.ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )


# TODO 删除的入参是ProfileID，需要在入参中设定
@router.delete(
    path=constants.ARCHIVES_URL,
    response_model=schemas.ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.10 人员档案删除接口",
)
async def archives_delete(): ...
