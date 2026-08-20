import tomllib
from pathlib import Path


def test_root_infrastructure_modules_move_under_core():
    root = Path(".")

    assert (root / "main.py").exists()

    expected_core_files = {
        "core/auth.py",
        "core/constants.py",
        "core/database.py",
        "core/exceptions.py",
        "core/settings.py",
        "core/utils.py",
    }

    for relative_path in expected_core_files:
        assert (root / relative_path).exists(), relative_path

    old_root_files = {
        "auth.py",
        "brokers.py",
        "constants.py",
        "database.py",
        "exceptions.py",
        "settings.py",
        "utils.py",
    }

    for relative_path in old_root_files:
        assert not (root / relative_path).exists(), relative_path

    assert not (root / "ingest").exists()
    assert not (root / "consumers").exists()


def test_pyproject_separates_runtime_and_development_dependencies():
    root = Path(".")
    config = tomllib.loads((root / "pyproject.toml").read_text())

    assert "build-system" not in config
    assert "project" not in config
    assert set(config["dependency-groups"]["runtime"]) == {
        "alembic",
        "asyncpg",
        "fastapi",
        "psycopg2-binary",
        "sqlmodel",
        "uvicorn",
    }
    dev_dependencies = config["dependency-groups"]["dev"]
    assert dev_dependencies[0] == {"include-group": "runtime"}
    assert set(dev_dependencies[1:]) == {
        "httpx",
        "pyright",
        "pytest",
        "pytest-asyncio",
        "ruff",
    }
    assert config["tool"]["pyright"]["pythonVersion"] == "3.14"
    assert config["tool"]["ruff"]["target-version"] == "py314"

    assert not (root / "requirements.txt").exists()
    assert not (root / "pyrightconfig.json").exists()
