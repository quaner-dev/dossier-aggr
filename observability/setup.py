from fastapi import FastAPI, Response

from database import engine

from .http import PrometheusHTTPMiddleware
from .layers import instrument_layers
from .metrics import render_metrics
from .sqlalchemy import instrument_sqlalchemy


def setup_observability(app: FastAPI) -> None:
    if getattr(app.state, "dossier_observability_ready", False):
        return

    instrument_sqlalchemy(engine.sync_engine)
    instrument_layers()

    app.add_middleware(PrometheusHTTPMiddleware)

    @app.get("/metrics", include_in_schema=False)
    async def metrics_endpoint() -> Response:
        return Response(
            content=render_metrics(),
            media_type="text/plain; version=0.0.4; charset=utf-8",
        )

    app.state.dossier_observability_ready = True
