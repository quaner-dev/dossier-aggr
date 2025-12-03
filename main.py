from typing import Any
from datetime import datetime

from fastapi import FastAPI, Depends

from sqlmodel import create_engine, select, Session

from contants import *
from schemas import *
from auth import HTTPDigest1400
import models

app = FastAPI()
engine = create_engine("sqlite:///db.sqlite3")
session = Session(engine)
security = HTTPDigest1400()


# TODO 这里的depends其实是Fastapi的设计模式，依赖注入，如果这样设定，Fastapi就可以正常运行这段代码，自动调用过__call__
@app.post(
    path=REGISTER_URL,
    response_model=ResponseStatusObject,
    dependencies=[Depends(security)],
)
async def register() -> Any:
    return {
        "RequestURL": REGISTER_URL,
        "StatusCode": "0",
        "StatusString": "注册成功",
        "LocalTime": datetime.now().strftime("%Y%m%d%H%M%S"),
    }


@app.post(path=UNREGISTER_URL, response_model=ResponseStatusObject)
async def unregister():
    return {
        "RequestURL": UNREGISTER_URL,
        "StatusCode": "0",
        "StatusString": "注销成功",
        "LocalTime": datetime.now().strftime("%Y%m%d%H%M%S"),
    }


@app.post(path=KEEPALIVE_URL, response_model=ResponseStatusObject)
async def keepalive():
    return {
        "RequestURL": KEEPALIVE_URL,
        "StatusCode": "0",
        "StatusString": "保活成功",
        "LocalTime": datetime.now().strftime("%Y%m%d%H%M%S"),
    }


@app.post(path=SUBSCRIBES_URL)
async def subscrbe(subscribe_list: SubscribeListObject):
    for subscribe in subscribe_list.SubscribeListObject.SubscribeObject:
        print(subscribe.BeginTime)
        session.add(
            models.Subscribe(
                SubscribeID=subscribe.SubscribeID,
                Title=subscribe.Title,
                SubscribeDetail=subscribe.SubscribeDetail,
                ResourceClass=subscribe.ResourceClass,
                ResourceURI=subscribe.ResourceURI,
                ApplicantName=subscribe.ApplicantName,
                ApplicantOrg=subscribe.ApplicantOrg,
                BeginTime=subscribe.BeginTime,
                EndTime=subscribe.EndTime,
                ReceiveAddr=subscribe.ReceiveAddr,
                ReportInterval=subscribe.ReportInterval,
                Reason=subscribe.Reason,
                OperateType=subscribe.OperateType,
                SubscribeStatus=subscribe.SubscribeStatus,
                SubscribeCancelOrg=subscribe.SubscribeCancelOrg,
                SubscribeCancelPerson=subscribe.SubscribeCancelPerson,
                CancelTime=subscribe.CancelTime,
                CancelReason=subscribe.CancelReason,
                ResultImageDeclare=subscribe.ResultImageDeclare,
                ResultFeatureDeclare=subscribe.ResultFeatureDeclare,
                TabID=subscribe.TabID,
            )
        )
        result = session.exec(
            select(models.Subscribe).where(
                models.Subscribe.SubscribeID == subscribe.SubscribeID
            )
        ).first()

        if result is None:
            raise Exception("aaa")


@app.get(path=APES_URL, response_model=ResponseStatusObject)
async def apes():
    results = session.exec(select(models.APE)).all()
    return {"APEListObject": {"APEObject": results}}
