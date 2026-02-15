import asyncio

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text

from database import engine

router = APIRouter()


@router.get("/startup", include_in_schema=False)
async def startup():
    return {"status": "starting"}


@router.get("/live", include_in_schema=False)
async def live() -> dict[str, str]:
    return {"status": "alive"}


@router.get("/ready", include_in_schema=False)
async def ready() -> JSONResponse:
    try:
        async with engine.connect() as connection:
            await asyncio.wait_for(connection.execute(text("SELECT 1")), timeout=1.5)
        return JSONResponse(status_code=200, content={"status": "ready"})
    except asyncio.TimeoutError:
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready"},
        )
    except Exception:
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready"},
        )
