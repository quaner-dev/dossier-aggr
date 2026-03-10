from pathlib import Path


def test_root_infrastructure_modules_move_under_core():
    root = Path(".")

    assert (root / "main.py").exists()

    expected_core_files = {
        "core/auth.py",
        "core/brokers.py",
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
