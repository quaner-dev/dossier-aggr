import subprocess
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
CHART = ROOT / "dossier-aggr"


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
    assert worker_env["ENV"] == api_env["ENV"]
    assert worker_env["RABBITMQ_IP"] == api_env["RABBITMQ_IP"]
    assert worker_env["DATABASE_URL"] == api_env["DATABASE_URL"]


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
