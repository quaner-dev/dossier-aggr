from .vehicle_archive import (
    list_vehicle_archives_task,
    create_vehicle_archives_task,
    update_vehicle_archives_task,
    delete_vehicle_archives_task,
)
from .vehicle_archive_subject import (
    query_vehicle_archive_subjects_task,
    create_vehicle_archive_subjects_task,
    update_vehicle_archive_subjects_task,
    delete_vehicle_archive_subjects_task,
)

__all__ = [
    "list_vehicle_archives_task",
    "create_vehicle_archives_task",
    "update_vehicle_archives_task",
    "delete_vehicle_archives_task",
    "query_vehicle_archive_subjects_task",
    "create_vehicle_archive_subjects_task",
    "update_vehicle_archive_subjects_task",
    "delete_vehicle_archive_subjects_task",
]
