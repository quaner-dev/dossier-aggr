# 从功能模块导入所有任务
from .collection.ape import (
    list_ape_task,
    update_apes_task,
)
from .collection.aps import list_apss_task
from .face.face import (
    get_face_task,
    list_faces_task,
    create_face_task,
    create_faces_task,
    update_face_task,
    delete_face_task,
)
from .person.person import (
    get_person_task,
    list_persons_task,
    create_person_task,
    create_persons_task,
    update_person_task,
    update_persons_task,
    delete_person_task,
    delete_persons_task,
)
from .subscribe.subscribe_notification import create_subscribe_notification


__all__ = [
    "list_ape_task",
    "update_apes_task",
    "list_apss_task",
    "get_face_task",
    "list_faces_task",
    "create_face_task",
    "create_faces_task",
    "update_face_task",
    "delete_face_task",
    "get_person_task",
    "list_persons_task",
    "create_person_task",
    "create_persons_task",
    "update_person_task",
    "update_persons_task",
    "delete_person_task",
    "delete_persons_task",
    "create_subscribe_notification",
]
