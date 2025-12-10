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
    response_model=schemas.ResponseStatusObject,
    dependencies=[Depends(security)],
)
async def register() -> Any:
    return {
        "RequestURL": constants.REGISTER_URL,
        "StatusCode": "0",
        "StatusString": "注册成功",
        "LocalTime": datetime.now().strftime("%Y%m%d%H%M%S"),
    }


@app.post(path=constants.UNREGISTER_URL, response_model=schemas.ResponseStatusObject)
async def unregister():
    return {
        "RequestURL": constants.UNREGISTER_URL,
        "StatusCode": "0",
        "StatusString": "注销成功",
        "LocalTime": datetime.now().strftime("%Y%m%d%H%M%S"),
    }


@app.post(path=constants.KEEPALIVE_URL, response_model=schemas.ResponseStatusObject)
async def keepalive():
    return {
        "RequestURL": constants.KEEPALIVE_URL,
        "StatusCode": "0",
        "StatusString": "保活成功",
        "LocalTime": datetime.now().strftime("%Y%m%d%H%M%S"),
    }


@app.post(
    path=constants.SUBSCRIBES_URL, response_model=schemas.ResponseStatusListObject
)
async def subscrbe(subscribe_list: schemas.SubscribeListObject):
    subscribes = subscribe_list.SubscribeListObject.SubscribeObject
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


@app.get(path=constants.APES_URL, response_model=schemas.APEListObject)
async def apes():
    apes = session.exec(select(models.APE)).all()
    return {"APEListObject": {"APEObject": apes}}


@app.post(
    path=constants.SUBSCRIBE_NOTIFICATIONS_URL,
    response_model=schemas.ResponseStatusObject,
)
async def subscribe_notifications():
    return {
        "RequestURL": constants.SUBSCRIBE_NOTIFICATIONS_URL,
        "StatusCode": "0",
        "StatusString": "OK",
        "LocalTime": datetime.now().strftime("%Y%m%d%H%M%S"),
    }


@app.post(path=constants.FACES_URL, response_model=schemas.ResponseStatusListObject)
async def face(face_list: schemas.FaceListObject):
    for face in face_list.FaceList:
        await tasks.my_redis_task.kiq(face)
