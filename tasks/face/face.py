import brokers
from models import Face
from repo.face.face import (
    create_face_repo,
    create_faces_repo,
    delete_face_repo,
    delete_faces_repo,
    get_face_repo,
    update_face_repo,
    update_faces_repo,
)


async def get_face_task(face_id: str) -> Face:
    return await get_face_repo(face_id=face_id)


@brokers.broker.task
async def create_face_task(face: Face):
    return await create_face_repo(face=face)


@brokers.broker.task
async def create_faces_task(faces: list[Face]):
    return await create_faces_repo(faces=faces)


@brokers.broker.task
async def update_face_task(face: Face):
    return await update_face_repo(face=face)


@brokers.broker.task
async def update_faces_task(faces: list[Face]):
    return await update_faces_repo(faces=faces)


@brokers.broker.task
async def delete_face_task(face_id: str):
    return await delete_face_repo(face_id=face_id)


@brokers.broker.task
async def delete_faces_task(face_ids: list[str]):
    return await delete_faces_repo(face_ids=face_ids)
