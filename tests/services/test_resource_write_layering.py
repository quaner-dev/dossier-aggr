import asyncio
from typing import Any, cast

from services.archive.archive_subject import ArchiveSubjectService
from services.archive.archives import ArchiveService
from services.face.face import FaceService
from services.person.person import PersonService
from services.subscribe.subscribe_notification import SubscribeNotificationService
from services.vehicle.vehicle_archive import VehicleArchiveService
from services.vehicle.vehicle_archive_subject import VehicleArchiveSubjectService


def test_resource_creates_call_repositories_directly(monkeypatch):
    async def _run() -> None:
        import services.archive.archive_subject as archive_subject_module
        import services.archive.archives as archives_module
        import services.face.face as face_module
        import services.person.person as person_module
        import services.subscribe.subscribe_notification as notification_module
        import services.vehicle.vehicle_archive as vehicle_archive_module
        import services.vehicle.vehicle_archive_subject as vehicle_subject_module

        values = cast(list[Any], [object(), object()])
        calls: list[str] = []

        async def fake_persons_repo(*, persons: list[Any]) -> list[Any]:
            calls.append("person")
            return persons

        async def fake_faces_repo(*, faces: list[Any]) -> list[Any]:
            calls.append("face")
            return faces

        async def fake_archives_repo(*, archives: list[Any]) -> list[Any]:
            calls.append("archive")
            return archives

        async def fake_subjects_repo(*, subjects: list[Any]) -> list[Any]:
            calls.append("archive_subject")
            return subjects

        monkeypatch.setattr(person_module, "create_persons_repo", fake_persons_repo)
        monkeypatch.setattr(face_module, "create_faces_repo", fake_faces_repo)
        monkeypatch.setattr(archives_module, "create_archives_repo", fake_archives_repo)
        monkeypatch.setattr(
            archive_subject_module, "create_archive_subjects_repo", fake_subjects_repo
        )
        monkeypatch.setattr(
            vehicle_archive_module, "create_vehicle_archives_repo", fake_archives_repo
        )
        monkeypatch.setattr(
            vehicle_subject_module,
            "create_vehicle_archive_subjects_repo",
            fake_subjects_repo,
        )

        async def fake_notifications_repo(
            *, subscribe_notifications: list[Any]
        ) -> list[Any]:
            calls.append("notification")
            return subscribe_notifications

        monkeypatch.setattr(
            notification_module,
            "create_subscribe_notifications_repo",
            fake_notifications_repo,
        )

        assert await PersonService().create_persons(values) is values
        assert await FaceService().create_faces(values) is values
        assert await ArchiveService().create_archives(values) == values
        assert await ArchiveSubjectService().create_archive_subjects(values) == values
        assert await VehicleArchiveService().create_vehicle_archives(values) == values
        assert (
            await VehicleArchiveSubjectService().create_vehicle_archive_subjects(values)
            == values
        )
        assert (
            await SubscribeNotificationService().create_subscribe_notifications(values)
            == values
        )
        assert calls == [
            "person",
            "face",
            "archive",
            "archive_subject",
            "archive",
            "archive_subject",
            "notification",
        ]

    asyncio.run(_run())


def test_person_and_face_services_return_write_results(monkeypatch):
    async def _run() -> None:
        import services.face.face as face_module
        import services.person.person as person_module

        person = cast(Any, object())
        face = cast(Any, object())
        persons = cast(list[Any], [person])
        faces = cast(list[Any], [face])

        async def fake_update_person_repo(*, person: Any) -> Any:
            return person

        async def fake_update_persons_repo(*, persons: list[Any]) -> list[Any]:
            return persons

        async def fake_delete_person_repo(*, person_id: str) -> str:
            return person_id

        async def fake_delete_persons_repo(*, person_ids: list[str]) -> list[str]:
            return person_ids

        async def fake_update_face_repo(*, face: Any) -> Any:
            return face

        async def fake_update_faces_repo(*, faces: list[Any]) -> list[Any]:
            return faces

        async def fake_delete_face_repo(*, face_id: str) -> str:
            return face_id

        async def fake_delete_faces_repo(*, face_ids: list[str]) -> list[str]:
            return face_ids

        monkeypatch.setattr(person_module, "update_person_repo", fake_update_person_repo)
        monkeypatch.setattr(person_module, "update_persons_repo", fake_update_persons_repo)
        monkeypatch.setattr(person_module, "delete_person_repo", fake_delete_person_repo)
        monkeypatch.setattr(person_module, "delete_persons_repo", fake_delete_persons_repo)
        monkeypatch.setattr(face_module, "update_face_repo", fake_update_face_repo)
        monkeypatch.setattr(face_module, "update_faces_repo", fake_update_faces_repo)
        monkeypatch.setattr(face_module, "delete_face_repo", fake_delete_face_repo)
        monkeypatch.setattr(face_module, "delete_faces_repo", fake_delete_faces_repo)

        assert await PersonService().update_person(person) is person
        assert await PersonService().update_persons(persons) is persons
        assert await PersonService().delete_person("person-1") == "person-1"
        assert await PersonService().delete_persons(["person-1"]) == ["person-1"]
        assert await FaceService().update_face(face) is face
        assert await FaceService().update_faces(faces) is faces
        assert await FaceService().delete_face("face-1") == "face-1"
        assert await FaceService().delete_faces(["face-1"]) == ["face-1"]

    asyncio.run(_run())
