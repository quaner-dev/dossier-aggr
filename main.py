from typing import Any
from datetime import datetime

from fastapi import FastAPI, Depends

from sqlmodel import create_engine, select, Session

from auth import HTTPDigest1400
import contants
import schemas
import models
import tasks
import arq

from contextlib import asynccontextmanager

redis: arq.connections.ArqRedis


@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis
    redis = await arq.create_pool(tasks.REDIS_SETTINGS)
    yield
    # 应用关闭时执行
    if redis:
        await redis.close()


app = FastAPI(lifespan=lifespan)
engine = create_engine("sqlite:///db.sqlite3")
session = Session(engine)
security = HTTPDigest1400()


@app.post(
    path=contants.REGISTER_URL,
    response_model=schemas.ResponseStatusObject,
    dependencies=[Depends(security)],
)
async def register() -> Any:
    return {
        "RequestURL": contants.REGISTER_URL,
        "StatusCode": "0",
        "StatusString": "注册成功",
        "LocalTime": datetime.now().strftime("%Y%m%d%H%M%S"),
    }


@app.post(path=contants.UNREGISTER_URL, response_model=schemas.ResponseStatusObject)
async def unregister():
    return {
        "RequestURL": contants.UNREGISTER_URL,
        "StatusCode": "0",
        "StatusString": "注销成功",
        "LocalTime": datetime.now().strftime("%Y%m%d%H%M%S"),
    }


@app.post(path=contants.KEEPALIVE_URL, response_model=schemas.ResponseStatusObject)
async def keepalive():
    return {
        "RequestURL": contants.KEEPALIVE_URL,
        "StatusCode": "0",
        "StatusString": "保活成功",
        "LocalTime": datetime.now().strftime("%Y%m%d%H%M%S"),
    }


@app.post(path=contants.SUBSCRIBES_URL, response_model=schemas.ResponseStatusListObject)
async def subscrbe(subscribe_list: schemas.SubscribeListObject):
    subscribes = subscribe_list.SubscribeListObject.SubscribeObject
    for subscribe in subscribes:
        session.add(models.Subscribe.model_validate(subscribe))

    session.commit()
    return {
        "ResponseStatusList": [
            {
                "RequestURL": contants.SUBSCRIBES_URL,
                "StatusCode": "0",
                "StatusString": "注册成功",
                "Id": subscribe.SubscribeID,
                "LocalTime": datetime.now().strftime("%Y%m%d%H%M%S"),
            }
            for subscribe in subscribes
        ]
    }


@app.get(path=contants.APES_URL, response_model=schemas.APEListObject)
async def apes():
    apes = session.exec(select(models.APE)).all()
    return {"APEListObject": {"APEObject": apes}}


@app.post(
    path=contants.SUBSCRIBE_NOTIFICATIONS_URL,
    response_model=schemas.ResponseStatusObject,
)
async def subscribe_notifications():
    global redis
    await redis.enqueue_job("test", "200")
    return {
        "RequestURL": contants.SUBSCRIBE_NOTIFICATIONS_URL,
        "StatusCode": "0",
        "StatusString": "OK",
        "LocalTime": datetime.now().strftime("%Y%m%d%H%M%S"),
    }


@app.post(path=contants.FACES_URL, response_model=schemas.ResponseStatusListObject)
async def face():
    pass
