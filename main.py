from fastapi import FastAPI

import taskiq_fastapi

from core import brokers
import api
from api.error_handlers import register_exception_handlers
from observability import setup_observability

taskiq_fastapi.init(brokers.broker, "main:app")


app = FastAPI(lifespan=brokers.lifespan)
setup_observability(app)
app.include_router(api.router)
register_exception_handlers(app)
