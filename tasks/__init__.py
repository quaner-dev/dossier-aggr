from .collection.aps import list_apss_task, update_aps_task
from .collection.ape import list_apes_task, update_apes_task
from .face.face import (
    get_face_task,
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

from .subscribe.subscribe import (
    create_subscribes_task,
    get_subscribe_task,
    list_subscribes_task,
    update_subscribe_by_id_task,
    update_subscribes_task,
    delete_subscribes_task,
)
from .subscribe.subscribe_notification import (
    create_subscribe_notifications_task,
    get_subscribe_notification_task,
)
from .library.archive_library import (
    list_archive_libraries_task,
    create_archive_libraries_task,
    update_archive_libraries_task,
    delete_archive_libraries_task,
)
from .archive.archives import (
    list_archives_task,
    create_archives_task,
    update_archives_task,
    delete_archives_task,
)
from .archive.archive_subject import (
    query_archive_subjects_task,
    create_archive_subjects_task,
    update_archive_subjects_task,
    delete_archive_subjects_task,
)
from .task.archive_task import (
    list_archive_tasks_task,
    create_archive_tasks_task,
    update_archive_tasks_task,
    delete_archive_tasks_task,
)
from .vehicle.vehicle_archive import (
    list_vehicle_archives_task,
    create_vehicle_archives_task,
    update_vehicle_archives_task,
    delete_vehicle_archives_task,
)
from .vehicle.vehicle_archive_subject import (
    query_vehicle_archive_subjects_task,
    create_vehicle_archive_subjects_task,
    update_vehicle_archive_subjects_task,
    delete_vehicle_archive_subjects_task,
)
from .verify.archive_confidence import verify_archive_confidence_task
from .verify.vehicle_archive_confidence import verify_vehicle_archive_confidence_task


__all__ = [
    # Collection
    "list_apss_task",
    "update_aps_task",
    "list_apes_task",
    "update_apes_task",
    # Face
    "get_face_task",
    "create_face_task",
    "create_faces_task",
    "update_face_task",
    "delete_face_task",
    # Person
    "get_person_task",
    "list_persons_task",
    "create_person_task",
    "create_persons_task",
    "update_person_task",
    "update_persons_task",
    "delete_person_task",
    "delete_persons_task",
    # Subscribe
    "list_subscribes_task",
    "create_subscribes_task",
    "get_subscribe_task",
    "update_subscribes_task",
    "update_subscribe_by_id_task",
    "delete_subscribes_task",
    # Subscribe Notification
    "create_subscribe_notifications_task",
    "get_subscribe_notification_task",
    # Archive Library
    "list_archive_libraries_task",
    "create_archive_libraries_task",
    "update_archive_libraries_task",
    "delete_archive_libraries_task",
    # Archives
    "list_archives_task",
    "create_archives_task",
    "update_archives_task",
    "delete_archives_task",
    "query_archive_subjects_task",
    "create_archive_subjects_task",
    "update_archive_subjects_task",
    "delete_archive_subjects_task",
    # Archive Task
    "list_archive_tasks_task",
    "create_archive_tasks_task",
    "update_archive_tasks_task",
    "delete_archive_tasks_task",
    # Vehicle Archive
    "list_vehicle_archives_task",
    "create_vehicle_archives_task",
    "update_vehicle_archives_task",
    "delete_vehicle_archives_task",
    # Vehicle Archive Subject
    "query_vehicle_archive_subjects_task",
    "create_vehicle_archive_subjects_task",
    "update_vehicle_archive_subjects_task",
    "delete_vehicle_archive_subjects_task",
    # Verify
    "verify_archive_confidence_task",
    "verify_vehicle_archive_confidence_task",
]
