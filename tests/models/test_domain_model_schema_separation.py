import importlib.util

from sqlmodel import SQLModel

import models
import schemas
from domain import (
    APE as APEDomain,
)
from domain import (
    APS as APSDomain,
)
from domain import (
    Archive as ArchiveDomain,
)
from domain import (
    ArchiveLibrary as ArchiveLibraryDomain,
)
from domain import (
    ArchiveSubject as ArchiveSubjectDomain,
)
from domain import (
    ArchiveTask as ArchiveTaskDomain,
)
from domain import (
    Face as FaceDomain,
)
from domain import (
    Person as PersonDomain,
)
from domain import (
    Subscribe as SubscribeDomain,
)
from domain import (
    SubscribeNotification as SubscribeNotificationDomain,
)
from domain import (
    VehicleArchive as VehicleArchiveDomain,
)
from domain import (
    VehicleArchiveSubject as VehicleArchiveSubjectDomain,
)
from schemas.archive.archive import Archive
from schemas.archive.archive_query import ArchiveQuery
from schemas.archive.archive_query_result import ArchiveQueryResult
from schemas.archive.archive_subject import ArchiveSubject
from schemas.archive.archive_subject_query import ArchiveSubjectQuery
from schemas.archive.archive_subject_query_result import ArchiveSubjectQueryResult
from schemas.archive.vehicle_archive import VehicleArchive
from schemas.archive.vehicle_archive_subject import VehicleArchiveSubject
from schemas.collection.ape import APEList
from schemas.collection.aps import APSList
from schemas.common.gait import Gait
from schemas.face.face import Face
from schemas.library.archive_library import ArchiveLibraryList
from schemas.person.person import Person
from schemas.subscribe.subscribe import SubscribeList
from schemas.subscribe.subscribe_notification import SubscribeNotification
from schemas.task.archive_task import ArchiveTaskList

DOMAIN_TABLE_PAIRS = (
    (APEDomain, models.APE),
    (APSDomain, models.APS),
    (ArchiveDomain, models.Archive),
    (ArchiveLibraryDomain, models.ArchiveLibrary),
    (ArchiveSubjectDomain, models.ArchiveSubject),
    (ArchiveTaskDomain, models.ArchiveTask),
    (FaceDomain, models.Face),
    (PersonDomain, models.Person),
    (SubscribeDomain, models.Subscribe),
    (SubscribeNotificationDomain, models.SubscribeNotification),
    (VehicleArchiveDomain, models.VehicleArchive),
    (VehicleArchiveSubjectDomain, models.VehicleArchiveSubject),
)


def test_table_models_inherit_domain_without_repeating_sqlmodel():
    for domain_type, table_type in DOMAIN_TABLE_PAIRS:
        assert table_type.__bases__ == (domain_type,)
        assert set(domain_type.model_fields) <= set(table_type.model_fields)


def test_http_schemas_are_non_table_sqlmodels():
    for name in schemas.__all__:
        schema_type = getattr(schemas, name)
        assert issubclass(schema_type, SQLModel)
        assert not hasattr(schema_type, "__table__")


def test_list_containers_are_only_exported_by_schemas():
    assert not any(name.endswith("List") for name in dir(__import__("domain")))
    assert any(name.endswith("List") for name in schemas.__all__)


def test_models_public_api_only_exports_table_models():
    assert all(issubclass(getattr(models, name), SQLModel) for name in models.__all__)
    assert not any(name.endswith("Schema") for name in models.__all__)


def test_all_table_models_are_registered_in_metadata():
    registered_types = {
        mapper.class_ for mapper in SQLModel._sa_registry.mappers  # type: ignore[attr-defined]
    }
    assert {table_type for _, table_type in DOMAIN_TABLE_PAIRS} <= registered_types


def test_schemas_are_split_into_corresponding_business_modules():
    schema_types = (
        Archive,
        ArchiveQuery,
        ArchiveQueryResult,
        ArchiveSubject,
        ArchiveSubjectQuery,
        ArchiveSubjectQueryResult,
        VehicleArchive,
        VehicleArchiveSubject,
        APEList,
        APSList,
        Gait,
        Face,
        ArchiveLibraryList,
        Person,
        SubscribeList,
        SubscribeNotification,
        ArchiveTaskList,
    )

    assert all(schema_type.__module__.startswith("schemas.") for schema_type in schema_types)
    assert importlib.util.find_spec("schemas.protocol") is None
