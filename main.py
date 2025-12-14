from typing import Any
from datetime import datetime

from fastapi import FastAPI, Depends
from sqlmodel import Session, create_engine, select

import taskiq_fastapi

import tasks
import models
import brokers
import schemas
import constants
from auth import HTTPDigest1400


taskiq_fastapi.init(brokers.broker, "main:app")


app = FastAPI(lifespan=brokers.lifespan)
engine = create_engine("sqlite:///db.sqlite3")
session = Session(engine)
security = HTTPDigest1400()


@app.post(
    path=constants.REGISTER_URL,
    response_model=schemas.ResponseStatus,
    dependencies=[Depends(security)],
    description="GA/T 1400.4-2017 7.2.1 注册消息",
)
async def register() -> Any:
    return {
        "RequestURL": constants.REGISTER_URL,
        "StatusCode": "0",
        "StatusString": "注册成功",
        "LocalTime": datetime.now().strftime("%Y%m%d%H%M%S"),
    }


@app.post(
    path=constants.UNREGISTER_URL,
    response_model=schemas.ResponseStatus,
    description="GA/T 1400.4-2017 7.2.2 注册消息",
)
async def unregister():
    return {
        "RequestURL": constants.UNREGISTER_URL,
        "StatusCode": "0",
        "StatusString": "注销成功",
        "LocalTime": datetime.now().strftime("%Y%m%d%H%M%S"),
    }


@app.post(
    path=constants.KEEPALIVE_URL,
    response_model=schemas.ResponseStatus,
    description="GA/T 1400.4-2017 7.2.3 保活消息",
)
async def keepalive():
    return {
        "RequestURL": constants.KEEPALIVE_URL,
        "StatusCode": "0",
        "StatusString": "保活成功",
        "LocalTime": datetime.now().strftime("%Y%m%d%H%M%S"),
    }


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
    return {
        "ResponseStatusList": [
            {
                "RequestURL": constants.SUBSCRIBES_URL,
                "StatusCode": "0",
                "StatusString": "注册成功",
                "Id": subscribe.SubscribeID,
                "LocalTime": datetime.now().strftime("%Y%m%d%H%M%S"),
            }
            for subscribe in subscribes
        ]
    }


@app.get(
    path=constants.APES_URL,
    response_model=schemas.APEListSchema,
    description="GA/T 1400.4-2017 7.2.5 采集设备的查询",
)
async def apes():
    apes = session.exec(select(models.APE)).all()
    return {"APEListObject": {"APEObject": apes}}


@app.post(
    path=constants.SUBSCRIBE_NOTIFICATIONS_URL,
    response_model=schemas.ResponseStatus,
    description="GA/T 1400.4-2017 7.2.21.1 通知消息",
)
async def subscribe_notifications():  # TODO 这里的请求体需要处理好
    return {
        "RequestURL": constants.SUBSCRIBE_NOTIFICATIONS_URL,
        "StatusCode": "0",
        "StatusString": "OK",
        "LocalTime": datetime.now().strftime("%Y%m%d%H%M%S"),
    }


@app.post(
    path=constants.FACES_URL,
    response_model=schemas.ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.12.1 人脸批量增加",
)
async def faces_create(data: schemas.FaceListObjectSchema):
    faces = data.FaceListObject.FaceObject
    for face in faces:
        await tasks.create_face.kiq(face)

    return {
        "ResponseStatusList": [
            {
                "RequestURL": constants.FACES_URL,
                "StatusCode": "0",
                "StatusString": "注册成功",
                "Id": face.FaceID,
                "LocalTime": datetime.now().strftime("%Y%m%d%H%M%S"),
            }
            for face in faces
        ]
    }


@app.post(
    path=constants.PERSONS_URL,
    response_model=schemas.ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.11.1 人脸人员增加",
)
async def persons_create(data: schemas.PersonListObjectSchema):
    persons = data.PersonListObject.PersonObject
    for person in persons:
        await tasks.create_person.kiq(person)

    return {
        "ResponseStatusList": [
            {
                "RequestURL": constants.PERSONS_URL,
                "StatusCode": "0",
                "StatusString": "注册成功",
                "Id": person.PersonID,
                "LocalTime": datetime.now().strftime("%Y%m%d%H%M%S"),
            }
            for person in persons
        ]
    }


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
async def archives_create(data: schemas.ArchiveListSchema): ...


@app.put(
    path=constants.ARCHIVES_URL,
    response_model=schemas.ResponseStatusListSchema,
    description="GA/T 2350.5-2025 A.10 人员档案更新接口",
)
async def archives_update(data: schemas.ArchiveListSchema): ...


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
