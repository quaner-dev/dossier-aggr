from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from models import (
    FaceList,
    FaceListObjectSchema,
    ResponseStatusListSchema,
    ResponseStatusList,
    ResponseStatus,
)
import constants
from services import FaceService

router = APIRouter()


# TODO 这里的内容需要进行补充，当前的检索逻辑其实没有完成属性键值对的条件检索
@router.get(
    path=constants.FACES_URL,
    response_model=FaceListObjectSchema,
    description="GA/T 1400.4-2017 7.2.12.1 人脸查询",
)
async def faces_query(
    service: Annotated[FaceService, Depends(FaceService)],
    face_id: str | None,
):
    """人脸查询接口"""
    if face_id:
        face = await service.get_face(face_id)
        return FaceListObjectSchema(FaceListObject=FaceList(FaceObject=[face]))
    else:
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
    for face in faces:
        _ = await service.update_face(face)

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

    for face_id in face_ids:
        await service.delete_face(face_id)

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
