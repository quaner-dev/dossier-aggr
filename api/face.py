from datetime import datetime

from fastapi import APIRouter, Depends, Query

from schemas import (
    ResponseStatusListSchema,
    FaceListObjectSchema,
    FaceList,
    ResponseStatus,
    ResponseStatusList,
)
import constants
from services import FaceService

router = APIRouter()


@router.get(
    path=constants.FACES_URL,
    response_model=FaceListSchema,
    description="GA/T 1400.4-2017 7.2.12.4 人脸查询",
)
async def faces_query(
    face_id: str | None = Query(None, alias="FaceID", max_length=33),
    service: FaceService = Depends(FaceService),
):
    """人脸查询接口"""
    if face_id:
        face = await service.get_face(face_id)
        return FaceListObjectSchema(FaceListObject=FaceList(FaceObject=[face]))
    else:
        faces = await service.list_faces()
        return FaceListObjectSchema(FaceListObject=FaceList(FaceObject=faces))


@router.post(
    path=constants.FACES_URL,
    response_model=ResponseStatusListSchema,
    description="GA/T 1400.4-2017 7.2.12.1 批量人脸增加",
)
async def faces_create(
    data: FaceListObjectSchema, service: FaceService = Depends(FaceService)
):
    """批量人脸增加接口"""
    faces = data.FaceListObject.FaceObject
    await service.batch_create_faces(faces)

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
    description="GA/T 1400.4-2017 7.2.12.2 批量人脸修改",
)
async def faces_update(
    data: FaceListObjectSchema,
    service: FaceService = Depends(FaceService),
):
    """批量人脸修改接口"""
    faces = data.FaceListObject.FaceObject
    for face in faces:
        await service.update_face(face.FaceID, face)

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
    description="GA/T 1400.4-2017 7.2.12.3 批量人脸删除",
)
async def faces_delete(
    id_list: str = Query(..., alias="IDList"),
    service: FaceService = Depends(FaceService),
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
