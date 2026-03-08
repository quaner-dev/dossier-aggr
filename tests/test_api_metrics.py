import asyncio

import httpx
from main import app


def test_metrics_endpoint_exposes_prometheus_text():
    async def _run():
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            # Generate baseline traffic.
            assert (await client.get("/live")).status_code == 200

            res = await client.get("/metrics")
            assert res.status_code == 200
            assert "text/plain" in res.headers.get("content-type", "")

            payload = res.text
            assert "dossier_aggr_http_requests_total" in payload
            assert "dossier_aggr_http_request_duration_seconds" in payload
            assert "dossier_aggr_http_in_progress_requests" in payload
            assert "dossier_aggr_orm_queries_total" in payload

    asyncio.run(_run())
