from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import taskiq_fastapi

import brokers
from models import ResponseStatusList, ResponseStatus
import exceptions
import api

# TODO
# 1. 将K8S中的内容迁移到helm创建的dossier-aggr中
# 2. 需要将接收到的信息，通过前端展示出来
# 3. 考量下imageid、sourceid是否不能重复，在数据库设计中是否需要加入uniq

taskiq_fastapi.init(brokers.broker, "main:app")


app = FastAPI(lifespan=brokers.lifespan)
app.include_router(api.router)


@app.exception_handler(exceptions.DataNotFoundError)
async def data_not_found_exception_handler(
    request: Request, exc: exceptions.DataNotFoundError
) -> JSONResponse:
    return JSONResponse(
        content=ResponseStatusList(
            ResponseStatusObject=ResponseStatus(
                RequestURL=str(request.url),
                StatusCode="9",
                StatusString=exc.detail,
                LocalTime=datetime.now(),
            )
        ).model_dump()
    )
