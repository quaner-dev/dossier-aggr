import pytest

from message.config import MessageConfig


def test_config_reads_environment_when_instance_is_created(monkeypatch):
    monkeypatch.setenv("OBJECT_STORAGE_PUBLIC_BASE_URL", "https://images.test")
    monkeypatch.setenv("OBJECT_STORAGE_BUCKET_PREFIX", "capture")

    config = MessageConfig()

    assert config.object_storage_public_base_url == "https://images.test"
    assert config.object_storage_bucket_prefix == "capture"


def test_config_requires_public_url_and_complete_credentials(monkeypatch):
    monkeypatch.delenv("OBJECT_STORAGE_PUBLIC_BASE_URL", raising=False)
    with pytest.raises(ValueError, match="PUBLIC_BASE_URL"):
        MessageConfig()

    monkeypatch.setenv("OBJECT_STORAGE_PUBLIC_BASE_URL", "https://images.test")
    monkeypatch.setenv("OBJECT_STORAGE_ACCESS_KEY_ID", "access")
    monkeypatch.delenv("OBJECT_STORAGE_SECRET_ACCESS_KEY", raising=False)
    with pytest.raises(ValueError, match="set together"):
        MessageConfig()
