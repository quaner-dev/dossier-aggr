from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends

import constants
from models import (
    Face,
    FaceList,
    FaceListObjectSchema,
    ResponseStatus,
    ResponseStatusList,
    ResponseStatusListSchema,
)
from services import FaceService

router = APIRouter()


@router.get(
    path=constants.FACES_URL,
    response_model=FaceListObjectSchema,
    description="GA/T 1400.4-2017 7.2.12.1 批量人脸查询",
)
async def faces_query(
    service: Annotated[FaceService, Depends(FaceService)],
):
    """批量人脸查询接口"""
    faces = await service.list_faces()

    return FaceListObjectSchema(
        FaceListObject=FaceList(FaceObject=[face for face in faces])
    )


@router.post(
    path=constants.FACES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.12.1 批量人脸增加",
)
async def faces_create(
    data: FaceListObjectSchema, service: Annotated[FaceService, Depends(FaceService)]
):
    """批量人脸增加接口"""
    faces = data.FaceListObject.FaceObject
    _ = await service.create_faces(faces)

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.FACES_URL,
            StatusCode="0",
            StatusString="上传成功",
            Id=face.FaceID,
            LocalTime=datetime.now(),
        )
        for face in faces
    ]

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )


@router.put(
    path=constants.FACES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.12.1 批量人脸修改",
)
async def faces_update(
    data: FaceListObjectSchema, service: Annotated[FaceService, Depends(FaceService)]
):
    """批量人脸修改接口"""
    faces = data.FaceListObject.FaceObject
    _ = await service.update_faces(faces)

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.FACES_URL,
            StatusCode="0",
            StatusString="修改成功",
            Id=face.FaceID,
            LocalTime=datetime.now(),
        )
        for face in faces
    ]

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )


@router.delete(
    path=constants.FACES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.12.1 批量人脸删除",
)
async def faces_delete(
    id_list: str,
    service: Annotated[FaceService, Depends(FaceService)],
):
    """批量人脸删除接口"""
    face_ids = [id.strip() for id in id_list.split(",")]
    _ = await service.delete_faces(face_ids)

    response_status_objects = [
        ResponseStatus(
            RequestURL=constants.FACES_URL,
            StatusCode="0",
            StatusString="删除成功",
            Id=face_id,
            LocalTime=datetime.now(),
        )
        for face_id in face_ids
    ]

    return ResponseStatusListSchema(
        ResponseStatusListObject=ResponseStatusList(
            ResponseStatusObject=response_status_objects
        )
    )


@router.get(
    path=f"{constants.FACES_URL}/{{face_id}}",
    response_model=Face,
    description="GA/T 1400.4-2017 7.2.12.2 单个人脸查询",
)
async def face_query(
    face_id: str,
    service: Annotated[FaceService, Depends(FaceService)],
) -> Face:
    """单个人脸查询接口"""
    face = await service.get_face(face_id)
    return face


@router.put(
    path=f"{constants.FACES_URL}/{{face_id}}",
    response_model=ResponseStatus,
    description="GA/T 1400.4-2017 7.2.12.2 单个人脸修改",
)
async def face_update(
    face_id: str,
    data: Face,
    service: Annotated[FaceService, Depends(FaceService)],
) -> ResponseStatus:
    """单个人脸修改接口"""
    data.FaceID = face_id
    _ = await service.update_face(data)
    return ResponseStatus(
        RequestURL=f"{constants.FACES_URL}/{face_id}",
        StatusCode="0",
        StatusString="修改成功",
        Id=face_id,
        LocalTime=datetime.now(),
    )


@router.delete(
    path=f"{constants.FACES_URL}/{{face_id}}",
    response_model=ResponseStatus,
    description="GA/T 1400.4-2017 7.2.12.2 单个人脸删除",
)
async def face_delete(
    face_id: str,
    service: Annotated[FaceService, Depends(FaceService)],
) -> ResponseStatus:
    """单个人脸删除接口"""
    _ = await service.delete_face(face_id)
    return ResponseStatus(
        RequestURL=f"{constants.FACES_URL}/{face_id}",
        StatusCode="0",
        StatusString="删除成功",
        Id=face_id,
        LocalTime=datetime.now(),
    )
