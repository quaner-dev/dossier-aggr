from time import perf_counter

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from .metrics import (
    HTTP_IN_PROGRESS,
    HTTP_REQUEST_DURATION_SECONDS,
    HTTP_REQUEST_SIZE_BYTES,
    HTTP_REQUESTS_TOTAL,
    HTTP_RESPONSE_SIZE_BYTES,
)


def _route_label(request: Request) -> str:
    route = request.scope.get("route")
    if route and getattr(route, "path", None):
        return route.path
    return request.url.path


def _header_int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        parsed = int(value)
    except ValueError:
        return None
    if parsed < 0:
        return None
    return parsed


class PrometheusHTTPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        method = request.method
        start = perf_counter()
        request_size = _header_int(request.headers.get("content-length"))
        status_code = "500"
        response: Response | None = None

        HTTP_IN_PROGRESS.inc()
        try:
            response = await call_next(request)
            status_code = str(response.status_code)
            return response
        finally:
            duration = perf_counter() - start
            route = _route_label(request)

            HTTP_IN_PROGRESS.dec()
            HTTP_REQUESTS_TOTAL.labels(
                method=method,
                route=route,
                status_code=status_code,
            ).inc()
            HTTP_REQUEST_DURATION_SECONDS.labels(
                method=method,
                route=route,
                status_code=status_code,
            ).observe(duration)

            if request_size is not None:
                HTTP_REQUEST_SIZE_BYTES.labels(method=method, route=route).observe(
                    request_size
                )

            if response is not None:
                response_size = _header_int(response.headers.get("content-length"))
                if response_size is not None:
                    HTTP_RESPONSE_SIZE_BYTES.labels(
                        method=method,
                        route=route,
                        status_code=status_code,
                    ).observe(response_size)
