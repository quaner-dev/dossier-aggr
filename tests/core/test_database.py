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
    for key in (
        "DATABASE_URL",
        "DB_POOL_SIZE",
        "DB_MAX_OVERFLOW",
        "DB_POOL_TIMEOUT_SECONDS",
        "DB_POOL_RECYCLE_SECONDS",
        "DB_POOL_PRE_PING",
    ):
        if key in env:
            monkeypatch.setenv(key, env[key])
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
        DATABASE_URL="postgresql+asyncpg://postgres:postgres@postgresql:5432/app",
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


def test_sqlite_engine_does_not_use_pool_options(
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
        DATABASE_URL="sqlite+aiosqlite:///db.sqlite3",
        DB_POOL_SIZE="7",
        DB_MAX_OVERFLOW="11",
        DB_POOL_TIMEOUT_SECONDS="3.5",
        DB_POOL_RECYCLE_SECONDS="1800",
        DB_POOL_PRE_PING="false",
    )

    assert captured["url"] == "sqlite+aiosqlite:///db.sqlite3"
    assert captured["kwargs"] == {}
