from pathlib import Path


def test_vehicle_archive_migration_exists():
    migration_dir = Path("alembic/versions")
    migration_files = list(migration_dir.glob("*.py"))
    assert migration_files

    has_vehicle_archive = any(
        "vehiclearchive" in file.read_text(encoding="utf-8")
        for file in migration_files
    )
    assert has_vehicle_archive


def test_archive_task_migration_exists():
    migration_dir = Path("alembic/versions")
    migration_files = list(migration_dir.glob("*.py"))
    assert migration_files

    has_archive_task = any(
        "archivetask" in file.read_text(encoding="utf-8") for file in migration_files
    )
    assert has_archive_task
