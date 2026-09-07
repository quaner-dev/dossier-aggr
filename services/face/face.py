from collections.abc import Sequence
from typing import Any
from fastapi import Request
from core import settings
from message.kafka import publish_message
from message.dispatch import MessageUnavailableError
from services.image_upload import transform_images

from domain import Face as FaceData
from models import Face
from repo.face.face import (
    create_face_repo,
    create_faces_repo,
    delete_face_repo,
    delete_faces_repo,
    get_face_repo,
    list_faces_repo,
    update_face_repo,
    update_faces_repo,
)
from schemas import FaceQueryParams
from services.model_conversion import to_table_model, to_table_models


class FaceService:
    """编排 GA/T 1400 人脸资源业务链路。

    读写请求统一委托 repo，保证请求完成时数据已经持久化。
    """

    async def get_face(self, face_id: str) -> Face:
        """根据FaceID查询人脸信息"""
        return await get_face_repo(face_id=face_id)

    async def list_faces(self, query: FaceQueryParams) -> list[Face]:
        return list(await list_faces_repo(query=query))

    async def create_face(self, face: FaceData) -> Face:
        return await create_face_repo(face=to_table_model(Face, face))

    async def create_faces(self, faces: Sequence[FaceData], *, request: Request | None = None, payload: dict[str, Any] | None = None) -> list[Face]:
        if request is not None:
            storage = getattr(request.app.state, "object_storage", None)
            producer = getattr(request.app.state, "kafka_producer", None)
            bucket = getattr(request.app.state, "object_storage_bucket_prefix", settings.OBJECT_STORAGE_BUCKET_PREFIX)
            if storage is None or producer is None or not bucket:
                raise MessageUnavailableError()
            body = payload or await request.json()
            await transform_images(body, storage=storage, bucket=bucket)
            await publish_message(producer=producer, topic="viid.faces.v1", payload=body)
            return []
        return await create_faces_repo(faces=to_table_models(Face, faces))

    async def update_face(self, face: FaceData) -> Face:
        return await update_face_repo(face=to_table_model(Face, face))

    async def update_faces(self, faces: Sequence[FaceData]) -> list[Face]:
        return await update_faces_repo(faces=to_table_models(Face, faces))

    async def delete_face(self, face_id: str) -> str:
        return await delete_face_repo(face_id=face_id)

    async def delete_faces(self, face_ids: list[str]) -> list[str]:
        return await delete_faces_repo(face_ids=face_ids)
