import logging
from typing import Any
from datetime import datetime

from fastapi import FastAPI, Depends
from sqlmodel import Session, create_engine, select

import taskiq_fastapi

import auth
import tasks
import models
import brokers
import schemas
import settings
import constants


taskiq_fastapi.init(brokers.broker, "main:app")


app = FastAPI(lifespan=brokers.lifespan)
engine = create_engine(settings.DATABASE_URL)
session = Session(engine)
security = auth.HTTPDigest1400()


@app.post(
    path=constants.REGISTER_URL,
    response_model=schemas.ResponseStatus,
    dependencies=[Depends(security)],
    description="GA/T 1400.4-2017 7.2.1 注册消息",
)
async def register() -> Any:
    response_status_object = schemas.ResponseStatus(
        RequestURL=constants.REGISTER_URL,
        StatusCode="0",
        StatusString="注册成功",
        LocalTime=datetime.now(),
    )
    return schemas.ResponseStatusList(ResponseStatusObject=response_status_object)


@app.post(
    path=constants.UNREGISTER_URL,
    response_model=schemas.ResponseStatus,
    description="GA/T 1400.4-2017 7.2.2 注册消息",
)
async def unregister():
    response_status_object = schemas.ResponseStatus(
        RequestURL=constants.UNREGISTER_URL,
        StatusCode="0",
        StatusString="注销成功",
        LocalTime=datetime.now(),
    )
    return schemas.ResponseStatusList(ResponseStatusObject=response_status_object)


@app.post(
    path=constants.KEEPALIVE_URL,
    response_model=schemas.ResponseStatus,
    description="GA/T 1400.4-2017 7.2.3 保活消息",
)
async def keepalive():
    response_status_object = schemas.ResponseStatus(
        RequestURL=constants.KEEPALIVE_URL,
        StatusCode="0",
        StatusString="保活成功",
        LocalTime=datetime.now(),
    )
    return schemas.ResponseStatusList(ResponseStatusObject=response_status_object)


@app.get(
    path=constants.APES_URL,
    response_model=schemas.APEListSchema,
    description="GA/T 1400.4-2017 7.2.5 采集设备的查询",
)
async def apes():
    apes = session.exec(select(models.APE)).all()
    return schemas.APEListSchema(APEListObject=schemas.APEList(APEObject=list(apes)))


@app.post(
    path=constants.PERSONS_URL,
    response_model=schemas.ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.11.1 人脸人员增加",
)
async def persons_create(data: schemas.PersonListObjectSchema):
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


@app.post(
    path=constants.FACES_URL,
    response_model=schemas.ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.12.1 人脸批量增加",
)
async def faces_create(data: schemas.FaceListObjectSchema):
    faces = data.FaceListObject.FaceObject
    for face in faces:
        await tasks.create_face.kiq(face)

    response_status_objects = [
        schemas.ResponseStatus(
            RequestURL=constants.FACES_URL,
            StatusCode="0",
            StatusString="上传成功",
            Id=face.FaceID,
            LocalTime=datetime.now(),
        )
        for face in faces
    ]

    return schemas.ResponseStatusListSchema(
        ResponseStatusListObject=schemas.ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )


@app.post(
    path=constants.SUBSCRIBES_URL,
    response_model=schemas.ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.20.1 批量订阅消息",
)
async def subscrbe(data: schemas.SubscribeListSchema):
    subscribes = data.SubscribeListObject.SubscribeObject
    for subscribe in subscribes:
        session.add(models.Subscribe.model_validate(subscribe))

    session.commit()

    response_status_objects = [
        schemas.ResponseStatus(
            RequestURL=constants.SUBSCRIBES_URL,
            StatusCode="0",
            StatusString="订阅成功",
            Id=subscribe.SubscribeID,
            LocalTime=datetime.now(),
        )
        for subscribe in subscribes
    ]

    return schemas.ResponseStatusListSchema(
        ResponseStatusListObject=schemas.ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )


@app.post(
    path=constants.SUBSCRIBE_NOTIFICATIONS_URL,
    response_model=schemas.ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.21.1 通知消息",
)
async def subscribe_notifications_create(
    data: schemas.SubscribeNotificationListSchema,
):
    subscribe_notifications = (
        data.SubscribeNotificationListObject.SubscribeNotificationObject
    )
    for subscribe_notification in subscribe_notifications:
        logging.info("Subscribe Notification: %s", subscribe_notification)

    response_status_objects = [
        schemas.ResponseStatus(
            RequestURL=constants.SUBSCRIBE_NOTIFICATIONS_URL,
            StatusCode="0",
            StatusString="通知成功",
            Id=subscribe_notification.NotificationID,
            LocalTime=datetime.now(),
        )
        for subscribe_notification in subscribe_notifications
    ]
    return schemas.ResponseStatusListSchema(
        ResponseStatusListObject=schemas.ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )


@app.get(
    path=constants.ARCHIVES_QUERY_SYNC_URL,
    response_model=schemas.ArchiveQueryResultSchema,
    description="GA/T 2350.5-2025 A.9 人员档案查询接口",
)
async def archives_query_sync_read(data: schemas.ArchiveQuerySchema): ...


@app.post(
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


@app.put(
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
@app.delete(
    path=constants.ARCHIVES_URL,
    response_model=schemas.ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.10 人员档案删除接口",
)
async def archives_delete(): ...


@app.post(
    path=constants.ARCHIVE_SUBJECT_QUERY_SYNC_URL,
    response_model="",
    description="GA/T 2350.5-2025 A.13 人员档案明细查询接口",
)
async def archive_subject_query_sync_read(data: schemas.ArchiveSubjectQuerySchema): ...
