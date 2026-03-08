from fastapi import FastAPI

import taskiq_fastapi

import brokers
import api
from api.error_handlers import register_exception_handlers
from observability import setup_observability

# TODO
# 1. 将K8S中的内容迁移到helm创建的dossier-aggr中
# 2. 需要将接收到的信息，通过前端展示出来
# 3. 考量下imageid、sourceid是否不能重复，在数据库设计中是否需要加入uniq

taskiq_fastapi.init(brokers.broker, "main:app")


app = FastAPI(lifespan=brokers.lifespan)
setup_observability(app)
app.include_router(api.router)
register_exception_handlers(app)
