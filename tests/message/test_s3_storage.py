import pytest
from botocore.exceptions import ClientError

from message.storage import S3CompatibleStorage


class FakeClient:
    def __init__(self):
        self.head_calls = []
        self.create_calls = []
        self.put_calls = []

    async def head_bucket(self, **kwargs):
        self.head_calls.append(kwargs)
        raise ClientError(
            {"Error": {"Code": "NoSuchBucket", "Message": "missing"}},
            "HeadBucket",
        )

    async def create_bucket(self, **kwargs):
        self.create_calls.append(kwargs)

    async def put_object(self, **kwargs):
        self.put_calls.append(kwargs)


class FakeClientContext:
    def __init__(self, client):
        self.client = client
        self.entered = False
        self.exited = False

    async def __aenter__(self):
        self.entered = True
        return self.client

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.exited = True


class FakeSession:
    def __init__(self, context):
        self.context = context
        self.calls = []

    def client(self, service_name, **kwargs):
        self.calls.append((service_name, kwargs))
        return self.context


@pytest.mark.asyncio
async def test_storage_creates_each_bucket_once_and_returns_stable_url():
    storage = S3CompatibleStorage(
        endpoint_url="http://storage:9000",
        public_base_url="https://images.example.test/base/",
    )
    client = FakeClient()
    storage._client = client

    first = await storage.upload(
        bucket="viid-20260901",
        content=b"one",
        content_type="image/jpeg",
    )
    second = await storage.upload(
        bucket="viid-20260901",
        content=b"two",
        content_type="image/jpeg",
    )

    assert client.head_calls == [{"Bucket": "viid-20260901"}]
    assert client.create_calls == [{"Bucket": "viid-20260901"}]
    assert len(client.put_calls) == 2
    assert first.startswith("https://images.example.test/base/viid-20260901/")
    assert second.startswith("https://images.example.test/base/viid-20260901/")


@pytest.mark.asyncio
async def test_storage_manages_client_lifecycle_with_exit_stack():
    storage = S3CompatibleStorage(
        endpoint_url="http://storage:9000",
        public_base_url="https://images.example.test",
    )
    client = FakeClient()
    context = FakeClientContext(client)
    session = FakeSession(context)
    storage._session = session

    await storage.start()

    assert storage._client is client
    assert context.entered is True
    assert session.calls == [
        (
            "s3",
            {
                "region_name": "us-east-1",
                "endpoint_url": "http://storage:9000",
            },
        )
    ]

    await storage.close()

    assert context.exited is True
    assert storage._client is None
