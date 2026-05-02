import asyncio

from models import Face, FaceQueryParams, Person
from repo.face import face as face_repo
from repo.person import person as person_repo


def _sample_person(person_id: str) -> Person:
    return Person(
        PersonID=person_id,
        SourceID=f"S-{person_id}",
        DeviceID="D-001",
        LeftTopX=1,
        LeftTopY=1,
        RightBtmX=10,
        RightBtmY=10,
    )


def _sample_face(face_id: str) -> Face:
    return Face(
        FaceID=face_id,
        SourceID=f"S-{face_id}",
        DeviceID="D-001",
        LeftTopX=1,
        LeftTopY=1,
        RightBtmX=10,
        RightBtmY=10,
    )


class _FakeResult:
    def __init__(self, obj):
        self._obj = obj

    def first(self):
        return self._obj

    def all(self):
        return self._obj


class _FakeAsyncSession:
    def __init__(self, found_obj):
        self.found_obj = found_obj
        self.deleted = None
        self.statement = None
        self.committed = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def exec(self, statement):
        self.statement = statement
        return _FakeResult(self.found_obj)

    async def delete(self, obj):
        self.deleted = obj

    async def commit(self):
        self.committed = True


def test_list_persons_repo_orders_and_limits_without_not_found(monkeypatch):
    async def _run():
        expected = [_sample_person("P-002"), _sample_person("P-001")]
        fake_session = _FakeAsyncSession(found_obj=expected)
        monkeypatch.setattr(person_repo, "AsyncSession", lambda _engine: fake_session)

        result = await person_repo.list_persons_repo()

        assert result == expected
        assert fake_session.statement is not None
        statement_text = str(fake_session.statement)
        assert "ORDER BY" in statement_text
        assert "PersonID" in statement_text
        assert "LIMIT" in statement_text
        assert "ASC" not in statement_text

    asyncio.run(_run())


def test_list_faces_repo_orders_without_default_limit(monkeypatch):
    async def _run():
        expected = [_sample_face("F-002"), _sample_face("F-001")]
        fake_session = _FakeAsyncSession(found_obj=expected)
        monkeypatch.setattr(face_repo, "AsyncSession", lambda _engine: fake_session)

        result = await face_repo.list_faces_repo(query=FaceQueryParams())

        assert result == expected
        assert fake_session.statement is not None
        statement_text = str(fake_session.statement)
        assert "ORDER BY" in statement_text
        assert "FaceID" in statement_text
        assert "LIMIT" not in statement_text
        assert "ASC" not in statement_text

    asyncio.run(_run())


def test_list_faces_repo_applies_pagination_query(monkeypatch):
    async def _run():
        expected = [_sample_face("F-002")]
        fake_session = _FakeAsyncSession(found_obj=expected)
        monkeypatch.setattr(face_repo, "AsyncSession", lambda _engine: fake_session)

        result = await face_repo.list_faces_repo(
            query=FaceQueryParams(RecordStartNo=1, PageRecordNum=1)
        )

        assert result == expected
        assert fake_session.statement is not None
        statement_text = str(fake_session.statement)
        assert "ORDER BY" in statement_text
        assert "FaceID" in statement_text
        assert "LIMIT" in statement_text
        assert "OFFSET" in statement_text

    asyncio.run(_run())


def test_delete_person_repo_deletes_by_person_id(monkeypatch):
    async def _run():
        expected = _sample_person("P-001")
        fake_session = _FakeAsyncSession(found_obj=expected)
        monkeypatch.setattr(person_repo, "AsyncSession", lambda _engine: fake_session)

        result = await person_repo.delete_person_repo(person_id="P-001")

        assert result == "P-001"
        assert fake_session.deleted is expected
        assert fake_session.committed is True
        assert fake_session.statement is not None
        assert "PersonID" in str(fake_session.statement)

    asyncio.run(_run())


def test_delete_face_repo_deletes_by_face_id(monkeypatch):
    async def _run():
        expected = _sample_face("F-001")
        fake_session = _FakeAsyncSession(found_obj=expected)
        monkeypatch.setattr(face_repo, "AsyncSession", lambda _engine: fake_session)

        result = await face_repo.delete_face_repo(face_id="F-001")

        assert result == "F-001"
        assert fake_session.deleted is expected
        assert fake_session.committed is True
        assert fake_session.statement is not None
        assert "FaceID" in str(fake_session.statement)

    asyncio.run(_run())
