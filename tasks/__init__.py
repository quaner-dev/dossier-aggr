# 从功能模块导入所有任务
from .face.face import create_face, create_faces
from .person.person import (
    get_person,
    list_persons,
    create_person,
    create_persons,
    update_person,
    update_persons,
    delete_person,
)
from .subscribe.subscribe_notification import create_subscribe_notification


__all__ = [
    "create_face",
    "create_faces",
    "get_person",
    "list_persons",
    "create_person",
    "create_persons",
    "update_person",
    "update_persons",
    "delete_person",
    "create_subscribe_notification",
]
