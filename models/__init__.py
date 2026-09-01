"""SQLModel table models registered in SQLModel.metadata."""

from .archive.archive import Archive
from .archive.archive_subject import ArchiveSubject
from .archive.vehicle_archive import VehicleArchive
from .archive.vehicle_archive_subject import VehicleArchiveSubject
from .collection.ape import APE
from .collection.aps import APS
from .face.face import Face
from .library.archive_library import ArchiveLibrary
from .person.person import Person
from .subscribe.subscribe import Subscribe
from .subscribe.subscribe_notification import SubscribeNotification
from .task.archive_task import ArchiveTask

__all__ = [
    "APE",
    "APS",
    "Archive",
    "ArchiveLibrary",
    "ArchiveSubject",
    "ArchiveTask",
    "Face",
    "Person",
    "Subscribe",
    "SubscribeNotification",
    "VehicleArchive",
    "VehicleArchiveSubject",
]
