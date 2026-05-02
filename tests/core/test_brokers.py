import importlib
import sys

import pytest
from taskiq_redis import RedisAsyncResultBackend


def _fresh_brokers_module(monkeypatch: pytest.MonkeyPatch, **env: str):
    for key in (
        "ENV",
        "RABBITMQ_USERNAME",
        "RABBITMQ_PASSWORD",
        "RABBITMQ_IP",
        "RABBITMQ_PORT",
        "TASKIQ_RESULT_BACKEND_URL",
    ):
        if key in env:
            monkeypatch.setenv(key, env[key])
        else:
            monkeypatch.delenv(key, raising=False)

    sys.modules.pop("core.brokers", None)
    sys.modules.pop("core.settings", None)
    core_package = sys.modules.get("core")
    if core_package is not None:
        for attr in ("brokers", "settings"):
            if hasattr(core_package, attr):
                delattr(core_package, attr)

    return importlib.import_module("core.brokers")


def test_production_broker_requires_shared_result_backend(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    with pytest.raises(RuntimeError, match="TASKIQ_RESULT_BACKEND_URL"):
        _fresh_brokers_module(monkeypatch, ENV="prod")


def test_production_broker_uses_redis_result_backend(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    brokers = _fresh_brokers_module(
        monkeypatch,
        ENV="prod",
        TASKIQ_RESULT_BACKEND_URL="redis://redis:6379/0",
    )

    assert isinstance(brokers.broker.result_backend, RedisAsyncResultBackend)
