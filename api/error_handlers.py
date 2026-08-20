from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from core import exceptions
from core.time import CHINA_TZ
from models import ResponseStatus, ResponseStatusList, ResponseStatusListSchema


def _detail_to_text(detail: object) -> str:
    if isinstance(detail, str):
        return detail
    if isinstance(detail, list):
        return "; ".join(str(item) for item in detail)
    return str(detail)


def _error_response(
    request: Request,
    *,
    http_status: int,
    status_code: str,
    status_string: str,
) -> JSONResponse:
    payload = ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=[
                ResponseStatus(
                    RequestURL=str(request.url),
                    StatusCode=status_code,
                    StatusString=status_string,
                    LocalTime=datetime.now(tz=CHINA_TZ),
                )
            ]
        )
    )
    return JSONResponse(status_code=http_status, content=payload.model_dump())


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(exceptions.DataNotFoundError)
    async def data_not_found_exception_handler(
        request: Request,
        exc: exceptions.DataNotFoundError,
    ) -> JSONResponse:
        return _error_response(
            request,
            http_status=exc.status_code,
            status_code="404",
            status_string=_detail_to_text(exc.detail),
        )

    @app.exception_handler(exceptions.DataAlreadyExistsError)
    async def data_already_exists_exception_handler(
        request: Request,
        exc: exceptions.DataAlreadyExistsError,
    ) -> JSONResponse:
        return _error_response(
            request,
            http_status=exc.status_code,
            status_code="409",
            status_string=_detail_to_text(exc.detail),
        )

    @app.exception_handler(exceptions.InvalidParameterError)
    async def invalid_parameter_exception_handler(
        request: Request,
        exc: exceptions.InvalidParameterError,
    ) -> JSONResponse:
        return _error_response(
            request,
            http_status=exc.status_code,
            status_code="400",
            status_string=_detail_to_text(exc.detail),
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return _error_response(
            request,
            http_status=400,
            status_code="400",
            status_string=_detail_to_text(exc.errors()),
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ) -> JSONResponse:
        return _error_response(
            request,
            http_status=exc.status_code,
            status_code=str(exc.status_code),
            status_string=_detail_to_text(exc.detail),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        return _error_response(
            request,
            http_status=500,
            status_code="500",
            status_string=_detail_to_text(exc),
        )
