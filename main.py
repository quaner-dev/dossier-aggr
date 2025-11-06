from typing import Any
from datetime import datetime


from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class VIIDHeaders(BaseModel):
    content_type: str = "application/VIID+JSON"


class ResponseStatusObject(BaseModel):
    RequestURL: str
    StatusCode: str
    StatusString: str
    LocalTime: str


@app.post(path="/VIID/System/Register", response_model=ResponseStatusObject)
async def create_register() -> Any:
    return {
        "RequestURL": "/VIID/System/Register",
        "StatusCode": "0",
        "StatusString": "注册成功",
        "LocalTime": datetime.now().strftime("%Y%m%d%H%M%S"),
    }


@app.post(path="/VIID/System/UnRegister")
async def unregister():
    pass


@app.post(path="/VIID/System/Keepalive")
async def keepalive():
    pass


@app.post(path="/VIID/Subscribes")
async def subscrbe():
    pass
