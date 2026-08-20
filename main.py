from fastapi import FastAPI

import api
from api.error_handlers import register_exception_handlers

app = FastAPI()
app.include_router(api.router)
register_exception_handlers(app)
