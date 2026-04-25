# 从功能模块导入所有services
from .collection.ape import APEService
from .collection.aps import APSService
from .person.person import PersonService
from .face.face import FaceService
from .subscribe.subscribe import SubscribeService
from .subscribe.subscribe_notification import SubscribeNotificationService
from .system.time import SystemTimeService

from .library.archive_library import ArchiveLibraryService
from .task.archive_task import ArchiveTaskService
from .archive.archives import ArchiveService
from .archive.archive_subject import ArchiveSubjectService
from .vehicle.vehicle_archive import VehicleArchiveService
from .vehicle.vehicle_archive_subject import VehicleArchiveSubjectService
from .verify.archive_confidence import ArchiveConfidenceService
from .verify.vehicle_archive_confidence import VehicleArchiveConfidenceService

__all__ = [
    "APEService",
    "APSService",
    "SubscribeService",
    "FaceService",
    "PersonService",
    "SubscribeNotificationService",
    "SystemTimeService",
    "ArchiveService",
    "ArchiveLibraryService",
    "ArchiveTaskService",
    "ArchiveSubjectService",
    "VehicleArchiveService",
    "VehicleArchiveSubjectService",
    "ArchiveConfidenceService",
    "VehicleArchiveConfidenceService",
]
