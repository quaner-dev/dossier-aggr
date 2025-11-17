from typing import Any
from datetime import datetime


from fastapi import FastAPI
from sqlmodel import create_engine, select, Session

from contants import *
from schemas import *
import models

app = FastAPI()
engine = create_engine("sqlite:///db.sqlite3")
session = Session(engine)


@app.post(path=register_url, response_model=ResponseStatusObject)
async def register() -> Any:
    return {
        "RequestURL": register_url,
        "StatusCode": "0",
        "StatusString": "注册成功",
        "LocalTime": datetime.now().strftime("%Y%m%d%H%M%S"),
    }


@app.post(path=unregister_url, response_model=ResponseStatusObject)
async def unregister():
    return {
        "RequestURL": unregister_url,
        "StatusCode": "0",
        "StatusString": "注销成功",
        "LocalTime": datetime.now().strftime("%Y%m%d%H%M%S"),
    }


@app.post(path=keepalive_url, response_model=ResponseStatusObject)
async def keepalive():
    return {
        "RequestURL": keepalive_url,
        "StatusCode": "0",
        "StatusString": "保活成功",
        "LocalTime": datetime.now().strftime("%Y%m%d%H%M%S"),
    }


@app.post(path=subscribe_url)
def subscrbe(subscribe_list: SubscribeListObject):
    for subscribe in subscribe_list.SubscribeListObject.SubscribeObject:
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
