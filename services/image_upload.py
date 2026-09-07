"""图片上传编排服务。

对象存储客户端只负责上传字节；协议 payload 的遍历、解码和字段替换
属于业务流程，因此集中在此处处理。
"""

import base64
import binascii
from collections.abc import Mapping
from typing import Any, Protocol


class ObjectStorage(Protocol):
    """Minimal adapter contract required by image transformation."""

    async def upload(self, *, bucket: str, content: bytes, content_type: str) -> str:
        ...


class ImageTransformError(ValueError):
    """请求中的图片无法转换或上传。"""


_CONTENT_TYPES = {
    "Bmp": "image/bmp",
    "Gif": "image/gif",
    "Jpeg": "image/jpeg",
    "Png": "image/png",
}


def _content_type(node: Mapping[str, Any]) -> str:
    file_format = node.get("FileFormat")
    if not isinstance(file_format, str):
        raise ImageTransformError("unsupported image FileFormat")
    try:
        return _CONTENT_TYPES[file_format]
    except KeyError as exc:
        raise ImageTransformError("unsupported image FileFormat") from exc


async def transform_images(
    payload: dict[str, Any], *, storage: ObjectStorage, bucket: str
) -> None:
    """上传 payload 中的图片并原地替换 StoragePath 和 Data。"""

    async def visit(value: Any) -> None:
        if isinstance(value, dict):
            if "Data" in value and "StoragePath" in value:
                data = value["Data"]
                if data is not None and data != "":
                    if not isinstance(data, str):
                        raise ImageTransformError("image Data must be a string")
                    try:
                        content = base64.b64decode(data, validate=True)
                    except (ValueError, binascii.Error) as exc:
                        raise ImageTransformError("invalid image Data") from exc
                    storage_path = await storage.upload(
                        bucket=bucket,
                        content=content,
                        content_type=_content_type(value),
                    )
                    if not storage_path or len(storage_path) > 256:
                        raise ImageTransformError("invalid storage path")
                    value["StoragePath"] = storage_path
                    value["Data"] = None
            for child in value.values():
                await visit(child)
        elif isinstance(value, list):
            for child in value:
                await visit(child)

    await visit(payload)
