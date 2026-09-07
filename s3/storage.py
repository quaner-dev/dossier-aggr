"""S3-compatible object-storage adapter."""

import asyncio
import uuid
from contextlib import AsyncExitStack
from typing import Any, cast

import aioboto3
from botocore.exceptions import ClientError


class S3CompatibleStorage:
    def __init__(
        self,
        *,
        endpoint_url: str,
        public_base_url: str,
        access_key: str = "",
        secret_key: str = "",
        region: str = "us-east-1",
    ) -> None:
        if not public_base_url.strip():
            raise ValueError("public base URL must not be empty")
        self._session = aioboto3.Session()
        self._kwargs: dict[str, str] = {"region_name": region}
        if endpoint_url:
            self._kwargs["endpoint_url"] = endpoint_url
        if access_key:
            self._kwargs.update(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
            )
        self._public_base_url = public_base_url.rstrip("/")
        self._exit_stack = AsyncExitStack()
        self._client: Any = None
        self._ready_buckets: set[str] = set()
        self._bucket_lock = asyncio.Lock()

    async def start(self) -> None:
        client_factory = cast(Any, self._session.client)
        self._client = await self._exit_stack.enter_async_context(
            client_factory("s3", **self._kwargs)
        )

    async def upload(self, *, bucket: str, content: bytes, content_type: str) -> str:
        if self._client is None:
            raise RuntimeError("storage is not started")
        await self._ensure_bucket(bucket)
        key = str(uuid.uuid4())
        await self._client.put_object(
            Bucket=bucket,
            Key=key,
            Body=content,
            ContentType=content_type,
        )
        return f"{self._public_base_url}/{bucket}/{key}"

    async def _ensure_bucket(self, bucket: str) -> None:
        if bucket in self._ready_buckets:
            return
        async with self._bucket_lock:
            if bucket in self._ready_buckets:
                return
            try:
                await self._client.head_bucket(Bucket=bucket)
            except ClientError as exc:
                code = str(exc.response.get("Error", {}).get("Code", ""))
                if code not in {"404", "NoSuchBucket", "NotFound"}:
                    raise
                await self._client.create_bucket(Bucket=bucket)
            self._ready_buckets.add(bucket)

    async def close(self) -> None:
        await self._exit_stack.aclose()
        self._client = None
        self._ready_buckets.clear()
