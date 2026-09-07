import pytest

from services.image_upload import ImageTransformError, transform_images


class FakeStorage:
    def __init__(self):
        self.calls = []

    async def start(self):
        pass

    async def upload(self, *, bucket, content, content_type):
        self.calls.append((bucket, content, content_type))
        return "images/item.jpg"

    async def close(self):
        pass


@pytest.mark.asyncio
async def test_transform_images_recurses_and_replaces_only_image_fields():
    storage = FakeStorage()
    payload = {
        "Images": [
            {"Data": "aGk=", "StoragePath": "", "FileFormat": "Jpeg", "Extra": 1}
        ]
    }
    await transform_images(payload, storage=storage, bucket="viid-20260901")
    assert payload["Images"][0]["Data"] is None
    assert payload["Images"][0]["StoragePath"] == "images/item.jpg"
    assert payload["Images"][0]["Extra"] == 1
    assert storage.calls == [("viid-20260901", b"hi", "image/jpeg")]


@pytest.mark.asyncio
async def test_empty_data_is_ignored():
    storage = FakeStorage()
    payload = {"Data": "", "StoragePath": "old", "FileFormat": "Png"}
    await transform_images(payload, storage=storage, bucket="viid-20260901")
    assert payload["Data"] == ""
    assert storage.calls == []


@pytest.mark.asyncio
async def test_invalid_data_and_format_fail():
    storage = FakeStorage()
    with pytest.raises(ImageTransformError):
        await transform_images(
            {"Data": "%%%", "StoragePath": "x", "FileFormat": "Png"},
            storage=storage,
            bucket="b",
        )
    with pytest.raises(ImageTransformError):
        await transform_images(
            {"Data": "aA==", "StoragePath": "x", "FileFormat": "Webp"},
            storage=storage,
            bucket="b",
        )
