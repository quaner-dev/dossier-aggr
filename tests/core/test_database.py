import importlib
import sys
from typing import Any

import pytest
from sqlalchemy.ext import asyncio as sqlalchemy_asyncio


def _fresh_database_module(
    monkeypatch: pytest.MonkeyPatch,
    fake_create_async_engine,
    **env: str,
):
    required_defaults = {
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "DB_USER": "postgres",
        "DB_PASSWORD": "postgres",
        "DB_NAME": "dossier_aggr",
    }
    for key in (
        "DB_HOST",
        "DB_PORT",
        "DB_USER",
        "DB_PASSWORD",
        "DB_NAME",
        "DB_POOL_SIZE",
        "DB_MAX_OVERFLOW",
        "DB_POOL_TIMEOUT_SECONDS",
        "DB_POOL_RECYCLE_SECONDS",
        "DB_POOL_PRE_PING",
    ):
        if key in env:
            monkeypatch.setenv(key, env[key])
        elif key in required_defaults:
            monkeypatch.setenv(key, required_defaults[key])
        else:
            monkeypatch.delenv(key, raising=False)

    sys.modules.pop("core.database", None)
    sys.modules.pop("core.settings", None)
    core_package = sys.modules.get("core")
    if core_package is not None:
        for attr in ("database", "settings"):
            if hasattr(core_package, attr):
                delattr(core_package, attr)

    monkeypatch.setattr(
        sqlalchemy_asyncio,
        "create_async_engine",
        fake_create_async_engine,
    )
    return importlib.import_module("core.database")


def test_postgresql_engine_uses_configured_pool_options(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    def fake_create_async_engine(url: str, **kwargs: Any) -> object:
        captured["url"] = url
        captured["kwargs"] = kwargs
        return object()

    _fresh_database_module(
        monkeypatch,
        fake_create_async_engine,
        DB_HOST="postgresql",
        DB_NAME="app",
        DB_POOL_SIZE="7",
        DB_MAX_OVERFLOW="11",
        DB_POOL_TIMEOUT_SECONDS="3.5",
        DB_POOL_RECYCLE_SECONDS="1800",
        DB_POOL_PRE_PING="false",
    )

    assert captured["url"].startswith("postgresql+asyncpg://")
    assert captured["kwargs"] == {
        "pool_size": 7,
        "max_overflow": 11,
        "pool_timeout": 3.5,
        "pool_recycle": 1800,
        "pool_pre_ping": False,
    }


def test_postgresql_engine_uses_default_pool_options_when_env_is_absent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    def fake_create_async_engine(url: str, **kwargs: Any) -> object:
        captured["url"] = url
        captured["kwargs"] = kwargs
        return object()

    _fresh_database_module(
        monkeypatch,
        fake_create_async_engine,
        DB_HOST="postgresql",
        DB_NAME="app",
    )

    assert captured["url"].startswith("postgresql+asyncpg://")
    assert captured["kwargs"] == {
        "pool_size": 10,
        "max_overflow": 20,
        "pool_timeout": 30.0,
        "pool_recycle": 1800,
        "pool_pre_ping": True,
    }


def test_default_database_url_uses_postgresql(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    def fake_create_async_engine(url: str, **kwargs: Any) -> object:
        captured["url"] = url
        captured["kwargs"] = kwargs
        return object()

    _fresh_database_module(monkeypatch, fake_create_async_engine)

    assert captured["url"] == (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/dossier_aggr"
    )


def test_database_url_is_built_from_connection_settings(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    def fake_create_async_engine(url: str, **kwargs: Any) -> object:
        captured["url"] = url
        return object()

    _fresh_database_module(
        monkeypatch,
        fake_create_async_engine,
        DB_HOST="database.internal",
        DB_PORT="5433",
        DB_USER="app_user",
        DB_PASSWORD="secret",
        DB_NAME="app",
    )

    assert captured["url"] == (
        "postgresql+asyncpg://app_user:secret@database.internal:5433/app"
    )


def test_db_pool_pre_ping_accepts_true_case_insensitively(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    def fake_create_async_engine(url: str, **kwargs: Any) -> object:
        captured["url"] = url
        captured["kwargs"] = kwargs
        return object()

    _fresh_database_module(
        monkeypatch,
        fake_create_async_engine,
        DB_HOST="postgresql",
        DB_NAME="app",
        DB_POOL_PRE_PING="TRUE",
    )

    assert captured["kwargs"]["pool_pre_ping"] is True


def test_postgresql_engine_always_uses_pool_options(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    def fake_create_async_engine(url: str, **kwargs: Any) -> object:
        captured["url"] = url
        captured["kwargs"] = kwargs
        return object()

    _fresh_database_module(
        monkeypatch,
        fake_create_async_engine,
        DB_HOST="postgresql",
        DB_NAME="app",
        DB_POOL_SIZE="7",
        DB_MAX_OVERFLOW="11",
        DB_POOL_TIMEOUT_SECONDS="3.5",
        DB_POOL_RECYCLE_SECONDS="1800",
        DB_POOL_PRE_PING="false",
    )

    assert captured["url"].startswith("postgresql+asyncpg://")
    assert captured["kwargs"] == {
        "pool_size": 7,
        "max_overflow": 11,
        "pool_timeout": 3.5,
        "pool_recycle": 1800,
        "pool_pre_ping": False,
    }
