import json
import subprocess
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
CHART = ROOT / "dossier-aggr"

PROTOCOL_BUSINESS_INTERFACES = {
    ("POST", "/VIID/System/Register"),
    ("POST", "/VIID/System/UnRegister"),
    ("POST", "/VIID/System/Keepalive"),
    ("GET", "/VIID/System/Time"),
    ("GET", "/VIID/APSs"),
    ("GET", "/VIID/APEs"),
    ("PUT", "/VIID/APEs"),
    ("GET", "/VIID/Faces"),
    ("POST", "/VIID/Faces"),
    ("PUT", "/VIID/Faces"),
    ("DELETE", "/VIID/Faces"),
    ("GET", "/VIID/Faces/{face_id}"),
    ("PUT", "/VIID/Faces/{face_id}"),
    ("DELETE", "/VIID/Faces/{face_id}"),
    ("GET", "/VIID/Persons"),
    ("POST", "/VIID/Persons"),
    ("PUT", "/VIID/Persons"),
    ("DELETE", "/VIID/Persons"),
    ("GET", "/VIID/Persons/{person_id}"),
    ("PUT", "/VIID/Persons/{person_id}"),
    ("DELETE", "/VIID/Persons/{person_id}"),
    ("POST", "/VIID/Subscribes"),
    ("GET", "/VIID/Subscribes"),
    ("PUT", "/VIID/Subscribes"),
    ("DELETE", "/VIID/Subscribes"),
    ("PUT", "/VIID/Subscribes/{subscribe_id}"),
    ("POST", "/VIID/SubscribeNotifications"),
    ("GET", "/VIID/SubscribeNotifications"),
    ("DELETE", "/VIID/SubscribeNotifications"),
    ("GET", "/VIID/ArchiveLibraries"),
    ("POST", "/VIID/ArchiveLibraries"),
    ("PUT", "/VIID/ArchiveLibraries"),
    ("DELETE", "/VIID/ArchiveLibraries"),
    ("GET", "/VIAS/Tasks"),
    ("POST", "/VIAS/Tasks"),
    ("PUT", "/VIAS/Tasks"),
    ("DELETE", "/VIAS/Tasks"),
    ("POST", "/VIID/ArchivesQuerySync"),
    ("POST", "/VIID/Archives"),
    ("PUT", "/VIID/Archives"),
    ("DELETE", "/VIID/Archives"),
    ("POST", "/VIID/ArchiveSubjectQuerySync"),
    ("POST", "/VIID/ArchiveSubjects"),
    ("PUT", "/VIID/ArchiveSubjects"),
    ("DELETE", "/VIID/ArchiveSubjects"),
    ("POST", "/VIID/VehicleArchivesQuerySync"),
    ("POST", "/VIID/VehicleArchives"),
    ("PUT", "/VIID/VehicleArchives"),
    ("DELETE", "/VIID/VehicleArchives"),
    ("POST", "/VIID/VehicleArchiveSubjectQuerySync"),
    ("POST", "/VIID/VehicleArchiveSubjects"),
    ("PUT", "/VIID/VehicleArchiveSubjects"),
    ("DELETE", "/VIID/VehicleArchiveSubjects"),
    ("POST", "/VIID/ArchiveConfidence"),
    ("POST", "/VIID/VehicleArchiveConfidence"),
}


def _render_chart(*args: str) -> list[dict[str, Any]]:
    completed = subprocess.run(
        ["helm", "template", "dossier-aggr-test", str(CHART), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return [
        document
        for document in yaml.safe_load_all(completed.stdout)
        if isinstance(document, dict)
    ]


def _by_kind_and_name(
    manifests: list[dict[str, Any]],
    kind: str,
    name: str,
) -> dict[str, Any]:
    for manifest in manifests:
        if manifest.get("kind") != kind:
            continue
        if manifest.get("metadata", {}).get("name") == name:
            return manifest
    raise AssertionError(f"{kind}/{name} not rendered")


def _container_env(manifest: dict[str, Any]) -> dict[str, str]:
    container = manifest["spec"]["template"]["spec"]["containers"][0]
    return {item["name"]: item["value"] for item in container.get("env", [])}


def _dashboard(manifests: list[dict[str, Any]]) -> dict[str, Any]:
    configmap = _by_kind_and_name(
        manifests,
        "ConfigMap",
        "dossier-aggr-test-grafana-dashboard",
    )
    return json.loads(configmap["data"]["dossier-aggr-overview.json"])


def test_service_only_selects_api_pods() -> None:
    manifests = _render_chart()

    service = _by_kind_and_name(manifests, "Service", "dossier-aggr-test")
    api = _by_kind_and_name(manifests, "Deployment", "dossier-aggr-test")
    worker = _by_kind_and_name(manifests, "Deployment", "dossier-aggr-test-worker")

    assert service["spec"]["selector"]["app.kubernetes.io/component"] == "api"
    assert (
        api["spec"]["selector"]["matchLabels"]["app.kubernetes.io/component"] == "api"
    )
    assert (
        api["spec"]["template"]["metadata"]["labels"]["app.kubernetes.io/component"]
        == "api"
    )
    assert (
        worker["spec"]["selector"]["matchLabels"]["app.kubernetes.io/component"]
        == "worker"
    )
    assert (
        worker["spec"]["template"]["metadata"]["labels"]["app.kubernetes.io/component"]
        == "worker"
    )


def test_default_chart_uses_production_broker_and_database_settings() -> None:
    manifests = _render_chart()

    api = _by_kind_and_name(manifests, "Deployment", "dossier-aggr-test")
    worker = _by_kind_and_name(manifests, "Deployment", "dossier-aggr-test-worker")

    api_env = _container_env(api)
    worker_env = _container_env(worker)

    assert api_env["ENV"] == "prod"
    assert api_env["RABBITMQ_IP"] == "rabbitmq"
    assert api_env["RABBITMQ_PORT"] == "5672"
    assert api_env["DATABASE_URL"].startswith("postgresql+asyncpg://")
    assert api_env["TASKIQ_RESULT_BACKEND_URL"].startswith("redis://")
    assert api_env["DB_POOL_SIZE"] == "10"
    assert api_env["DB_MAX_OVERFLOW"] == "20"
    assert api_env["DB_POOL_TIMEOUT_SECONDS"] == "30"
    assert api_env["DB_POOL_RECYCLE_SECONDS"] == "1800"
    assert api_env["DB_POOL_PRE_PING"] == "true"
    assert worker_env["ENV"] == api_env["ENV"]
    assert worker_env["RABBITMQ_IP"] == api_env["RABBITMQ_IP"]
    assert worker_env["DATABASE_URL"] == api_env["DATABASE_URL"]
    assert worker_env["TASKIQ_RESULT_BACKEND_URL"] == api_env["TASKIQ_RESULT_BACKEND_URL"]
    for key in (
        "DB_POOL_SIZE",
        "DB_MAX_OVERFLOW",
        "DB_POOL_TIMEOUT_SECONDS",
        "DB_POOL_RECYCLE_SECONDS",
        "DB_POOL_PRE_PING",
    ):
        assert worker_env[key] == api_env[key]

    worker_container = worker["spec"]["template"]["spec"]["containers"][0]
    assert worker_container["args"] == ["worker", "core.brokers:broker", "tasks"]


def test_chart_renders_alembic_upgrade_job() -> None:
    manifests = _render_chart()

    job = _by_kind_and_name(manifests, "Job", "dossier-aggr-test-migrations")
    annotations = job["metadata"].get("annotations", {})
    container = job["spec"]["template"]["spec"]["containers"][0]

    assert "pre-install" in annotations["helm.sh/hook"]
    assert "pre-upgrade" in annotations["helm.sh/hook"]
    assert container["command"] == ["alembic"]
    assert container["args"] == ["upgrade", "head"]
    assert _container_env(job)["ENV"] == "prod"


def test_runtime_pods_can_load_environment_from_external_secret() -> None:
    manifests = _render_chart(
        "--set",
        "envFrom[0].secretRef.name=dossier-aggr-runtime",
    )

    api = _by_kind_and_name(manifests, "Deployment", "dossier-aggr-test")
    worker = _by_kind_and_name(manifests, "Deployment", "dossier-aggr-test-worker")
    job = _by_kind_and_name(manifests, "Job", "dossier-aggr-test-migrations")

    expected = [{"secretRef": {"name": "dossier-aggr-runtime"}}]
    assert api["spec"]["template"]["spec"]["containers"][0]["envFrom"] == expected
    assert worker["spec"]["template"]["spec"]["containers"][0]["envFrom"] == expected
    assert job["spec"]["template"]["spec"]["containers"][0]["envFrom"] == expected


def test_monitoring_dashboard_breaks_http_metrics_down_by_interface() -> None:
    manifests = _render_chart()

    panels = {panel["title"]: panel for panel in _dashboard(manifests)["panels"]}

    qps_expr = panels["HTTP QPS by Interface"]["targets"][0]["expr"]
    assert "sum by (method, route)" in qps_expr
    assert 'dossier_aggr_http_requests_total' in qps_expr
    assert panels["HTTP QPS by Interface"]["targets"][0]["legendFormat"] == (
        "{{method}} {{route}}"
    )

    error_ratio_expr = panels["HTTP 5xx Ratio by Interface"]["targets"][0]["expr"]
    assert "sum by (method, route)" in error_ratio_expr
    assert 'status_code=~"5.."' in error_ratio_expr
    assert "clamp_min" in error_ratio_expr

    latency_expr = panels["HTTP P95 Latency by Interface"]["targets"][0]["expr"]
    assert "histogram_quantile(0.95" in latency_expr
    assert "by (le, method, route)" in latency_expr


def test_prometheus_rule_adds_route_level_alerts_for_critical_interfaces() -> None:
    manifests = _render_chart("--set", "monitoring.prometheusRule.enabled=true")

    rule = _by_kind_and_name(manifests, "PrometheusRule", "dossier-aggr-test")
    rules = {
        item["alert"]: item
        for item in rule["spec"]["groups"][0]["rules"]
        if "alert" in item
    }

    register_error = rules["DossierAggrRouteHighErrorRateSystemRegister"]["expr"]
    assert 'method="POST",route="/VIID/System/Register"' in register_error
    assert 'status_code=~"5.."' in register_error
    assert "clamp_min" in register_error

    notification_latency = rules[
        "DossierAggrRouteHighP95LatencySubscribeNotificationCreate"
    ]["expr"]
    assert 'method="POST",route="/VIID/SubscribeNotifications"' in notification_latency
    assert "histogram_quantile" in notification_latency


def test_prometheus_route_alerts_cover_all_protocol_business_interfaces() -> None:
    manifests = _render_chart("--set", "monitoring.prometheusRule.enabled=true")

    rule = _by_kind_and_name(manifests, "PrometheusRule", "dossier-aggr-test")
    rules = [
        item
        for item in rule["spec"]["groups"][0]["rules"]
        if item.get("alert", "").startswith("DossierAggrRoute")
    ]

    error_alert_interfaces = {
        (item["labels"]["method"], item["labels"]["route"])
        for item in rules
        if item["alert"].startswith("DossierAggrRouteHighErrorRate")
    }
    latency_alert_interfaces = {
        (item["labels"]["method"], item["labels"]["route"])
        for item in rules
        if item["alert"].startswith("DossierAggrRouteHighP95Latency")
    }

    assert error_alert_interfaces == PROTOCOL_BUSINESS_INTERFACES
    assert latency_alert_interfaces == PROTOCOL_BUSINESS_INTERFACES


def test_dev_values_keep_lightweight_sqlite_profile() -> None:
    manifests = _render_chart("-f", str(CHART / "values-dev.yaml"))

    api = _by_kind_and_name(manifests, "Deployment", "dossier-aggr-test")
    api_env = _container_env(api)

    assert api_env["ENV"] == "dev"
    assert api_env["DATABASE_URL"].startswith("sqlite+aiosqlite:///")

    kinds_and_names = {
        (manifest.get("kind"), manifest.get("metadata", {}).get("name"))
        for manifest in manifests
    }
    assert ("Deployment", "dossier-aggr-test-worker") not in kinds_and_names
