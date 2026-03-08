# 1400 + 2350 Contract Completion Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Deliver protocol-complete 1400 + 2350 interfaces and object behavior with contract-first tests as release gates.

**Architecture:** Keep current layered design (`api -> services -> tasks -> models`) and implement missing clauses by vertical slices. Each clause is completed with test-first flow: failing protocol test -> minimal implementation -> pass tests -> commit. Keep protocol wrappers and `YYYYMMDDHHMMSS` time format consistent.

**Tech Stack:** FastAPI, SQLModel, Taskiq, Alembic, pytest, SQLite (tests), PostgreSQL (runtime)

---

### Task 1: Build protocol conformance matrix as executable backlog

**Files:**
- Create: `tests/protocol/test_protocol_matrix_guard.py`
- Modify: `.docs/PROTOCOL_1400.md`
- Modify: `.docs/PROTOCOL_2350.md`

**Step 1: Write the failing test**

```python
from pathlib import Path

def test_protocol_docs_cover_all_2350_clauses():
    p = Path('.docs/PROTOCOL_2350.md').read_text(encoding='utf-8')
    for clause in ['A.5','A.6','A.7','A.8','A.9','A.10','A.11','A.12','A.13','A.14','A.15','A.16','A.17','A.18']:
        assert clause in p
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/protocol/test_protocol_matrix_guard.py::test_protocol_docs_cover_all_2350_clauses -v`
Expected: FAIL (missing clauses in current protocol doc)

**Step 3: Write minimal implementation**

Update `.docs/PROTOCOL_2350.md` to explicitly list A.5-A.18 and all URI resources.

**Step 4: Run test to verify it passes**

Run: `pytest tests/protocol/test_protocol_matrix_guard.py::test_protocol_docs_cover_all_2350_clauses -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/protocol/test_protocol_matrix_guard.py .docs/PROTOCOL_2350.md .docs/PROTOCOL_1400.md
git commit -m "docs: align 1400/2350 protocol clause matrix"
```

### Task 2: Stabilize high-risk 1400 behaviors before 2350 expansion

**Files:**
- Modify: `tasks/person/person.py`
- Modify: `services/face/face.py`
- Modify: `tasks/face/face.py`
- Test: `tests/api/test_person_api.py`
- Test: `tests/api/test_face_api.py`

**Step 1: Write the failing tests**

```python
async def test_delete_persons_deletes_by_person_id(...):
    ...

async def test_delete_faces_accepts_face_id_list(...):
    ...
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/api/test_person_api.py::test_delete_persons_deletes_by_person_id tests/api/test_face_api.py::test_delete_faces_accepts_face_id_list -v`
Expected: FAIL with deletion behavior mismatch

**Step 3: Write minimal implementation**

- Use `select + delete` by business ID in person delete task.
- Align `FaceService.delete_face` signature and task payload.

**Step 4: Run tests to verify they pass**

Run: `pytest tests/api/test_person_api.py tests/api/test_face_api.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tasks/person/person.py services/face/face.py tasks/face/face.py tests/api/test_person_api.py tests/api/test_face_api.py
git commit -m "fix: align person and face delete behavior with protocol ids"
```

### Task 3: Implement 2350 A.5 ArchiveLibrary endpoints end-to-end

**Files:**
- Modify: `constants.py`
- Modify: `api/library/archive_library.py`
- Modify: `services/library/archive_library.py`
- Create: `tasks/library/archive_library.py`
- Modify: `tasks/__init__.py`
- Test: `tests/api/test_archive_library_api.py`

**Step 1: Write the failing tests**

```python
async def test_archive_library_crud_contract(...):
    ...
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/api/test_archive_library_api.py::test_archive_library_crud_contract -v`
Expected: FAIL (route/service/task skeleton)

**Step 3: Write minimal implementation**

- Add list/create/update/delete logic via service + task.
- Return `ResponseStatusListSchema` with one status per input item.

**Step 4: Run test to verify it passes**

Run: `pytest tests/api/test_archive_library_api.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add constants.py api/library/archive_library.py services/library/archive_library.py tasks/library/archive_library.py tasks/__init__.py tests/api/test_archive_library_api.py
git commit -m "feat: implement 2350 A.5 archive library interfaces"
```

### Task 4: Implement 2350 A.9/A.10 Archive query + CRUD

**Files:**
- Modify: `api/archive/archives.py`
- Modify: `services/archive/archives.py`
- Create: `tasks/archive/archives.py`
- Modify: `tasks/__init__.py`
- Test: `tests/api/test_archives_api.py`

**Step 1: Write the failing tests**

```python
async def test_archives_query_sync_returns_archive_query_result(...):
    ...

async def test_archives_crud_returns_status_list(...):
    ...
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/api/test_archives_api.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

- Implement query sync endpoint with `ArchiveQuerySchema -> ArchiveQueryResultSchema` mapping.
- Implement POST/PUT/DELETE with service/task and status list response.

**Step 4: Run test to verify it passes**

Run: `pytest tests/api/test_archives_api.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add api/archive/archives.py services/archive/archives.py tasks/archive/archives.py tasks/__init__.py tests/api/test_archives_api.py
git commit -m "feat: implement 2350 A.9 A.10 archives query and CRUD"
```

### Task 5: Implement 2350 A.13/A.14 ArchiveSubject query + CRUD

**Files:**
- Modify: `api/archive/archive_subject.py`
- Modify: `services/archive/archive_subject.py`
- Create: `tasks/archive/archive_subject.py`
- Modify: `tasks/__init__.py`
- Test: `tests/api/test_archive_subject_api.py`

**Step 1: Write the failing tests**

```python
async def test_archive_subject_query_sync_contract(...):
    ...

async def test_archive_subject_crud_contract(...):
    ...
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/api/test_archive_subject_api.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

- Implement query sync + create/update/delete behavior.
- Parse list query params with shared parser.

**Step 4: Run test to verify it passes**

Run: `pytest tests/api/test_archive_subject_api.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add api/archive/archive_subject.py services/archive/archive_subject.py tasks/archive/archive_subject.py tasks/__init__.py tests/api/test_archive_subject_api.py
git commit -m "feat: implement 2350 A.13 A.14 archive subject interfaces"
```

### Task 6: Add missing 2350 constants/routes for A.6/A.11/A.12/A.15/A.16/A.17/A.18

**Files:**
- Modify: `constants.py`
- Modify: `api/__init__.py`
- Create: `api/task/archive_task.py`
- Create: `api/vehicle/vehicle_archive.py`
- Create: `api/vehicle/vehicle_archive_subject.py`
- Create: `api/verify/archive_confidence.py`
- Create: `api/verify/vehicle_archive_confidence.py`
- Test: `tests/protocol/test_2350_routes.py`

**Step 1: Write the failing test**

```python
def test_2350_routes_registered_on_openapi(client):
    paths = client.get('/openapi.json').json()['paths'].keys()
    for p in [
        '/VIAS/Tasks',
        '/VIID/VehicleArchives',
        '/VIID/VehicleArchivesQuerySync',
        '/VIID/VehicleArchiveSubjects',
        '/VIID/VehicleArchiveSubjectQuerySync',
        '/VIID/ArchiveConfidence',
        '/VIID/VehicleArchiveConfidence',
    ]:
        assert p in paths
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/protocol/test_2350_routes.py::test_2350_routes_registered_on_openapi -v`
Expected: FAIL

**Step 3: Write minimal implementation**

- Add missing constants.
- Add route modules and include routers.

**Step 4: Run test to verify it passes**

Run: `pytest tests/protocol/test_2350_routes.py::test_2350_routes_registered_on_openapi -v`
Expected: PASS

**Step 5: Commit**

```bash
git add constants.py api/__init__.py api/task/archive_task.py api/vehicle/vehicle_archive.py api/vehicle/vehicle_archive_subject.py api/verify/archive_confidence.py api/verify/vehicle_archive_confidence.py tests/protocol/test_2350_routes.py
git commit -m "feat: add missing 2350 route and constant skeletons"
```

### Task 7: Implement missing 2350 models B.4 and B.16 (+ wrappers)

**Files:**
- Create: `models/archive/vehicle_archive.py`
- Create: `models/archive/vehicle_archive_subject.py`
- Create: `models/common/gait.py`
- Modify: `models/__init__.py`
- Test: `tests/models/test_2350_models.py`

**Step 1: Write the failing tests**

```python
def test_vehicle_archive_model_validate_roundtrip():
    ...

def test_gait_model_schema_contains_expected_fields():
    ...
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/models/test_2350_models.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

- Add SQLModel/Pydantic models per protocol fields.
- Export via `models/__init__.py`.

**Step 4: Run test to verify it passes**

Run: `pytest tests/models/test_2350_models.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add models/archive/vehicle_archive.py models/archive/vehicle_archive_subject.py models/common/gait.py models/__init__.py tests/models/test_2350_models.py
git commit -m "feat: add 2350 vehicle archive and gait models"
```

### Task 8: Add Alembic migration for new persistent entities

**Files:**
- Create: `alembic/versions/<revision>_add_vehicle_archive_tables.py`
- Test: `tests/migrations/test_upgrade_head.py`

**Step 1: Write the failing test**

```python
def test_alembic_upgrade_head_runs_cleanly():
    ...
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/migrations/test_upgrade_head.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

- Generate and adjust migration to create new tables/indexes.
- Ensure downgrade is reversible.

**Step 4: Run test to verify it passes**

Run: `pytest tests/migrations/test_upgrade_head.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add alembic/versions/*.py tests/migrations/test_upgrade_head.py
git commit -m "feat: add migration for 2350 vehicle archive persistence"
```

### Task 9: Implement A.6 Task CRUD (VIAS Tasks)

**Files:**
- Create: `models/task/archive_task.py`
- Create: `services/task/archive_task.py`
- Create: `tasks/task/archive_task.py`
- Modify: `api/task/archive_task.py`
- Modify: `services/__init__.py`
- Modify: `tasks/__init__.py`
- Test: `tests/api/test_archive_task_api.py`

**Step 1: Write the failing tests**

```python
async def test_archive_task_crud_contract(...):
    ...
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/api/test_archive_task_api.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

- Implement CRUD paths and response wrappers per protocol.

**Step 4: Run test to verify it passes**

Run: `pytest tests/api/test_archive_task_api.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add models/task/archive_task.py services/task/archive_task.py tasks/task/archive_task.py api/task/archive_task.py services/__init__.py tasks/__init__.py tests/api/test_archive_task_api.py
git commit -m "feat: implement 2350 A.6 archive task interfaces"
```

### Task 10: Implement A.11/A.12/A.15/A.16 vehicle archive interfaces

**Files:**
- Modify: `api/vehicle/vehicle_archive.py`
- Modify: `api/vehicle/vehicle_archive_subject.py`
- Create: `services/vehicle/vehicle_archive.py`
- Create: `services/vehicle/vehicle_archive_subject.py`
- Create: `tasks/vehicle/vehicle_archive.py`
- Create: `tasks/vehicle/vehicle_archive_subject.py`
- Modify: `services/__init__.py`
- Modify: `tasks/__init__.py`
- Test: `tests/api/test_vehicle_archive_api.py`
- Test: `tests/api/test_vehicle_archive_subject_api.py`

**Step 1: Write the failing tests**

```python
async def test_vehicle_archive_query_and_crud_contract(...):
    ...

async def test_vehicle_archive_subject_query_and_crud_contract(...):
    ...
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/api/test_vehicle_archive_api.py tests/api/test_vehicle_archive_subject_api.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

- Implement vehicle archive and vehicle archive subject query + CRUD paths.

**Step 4: Run test to verify it passes**

Run: `pytest tests/api/test_vehicle_archive_api.py tests/api/test_vehicle_archive_subject_api.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add api/vehicle/vehicle_archive.py api/vehicle/vehicle_archive_subject.py services/vehicle/*.py tasks/vehicle/*.py services/__init__.py tasks/__init__.py tests/api/test_vehicle_archive_api.py tests/api/test_vehicle_archive_subject_api.py
git commit -m "feat: implement 2350 vehicle archive and subject interfaces"
```

### Task 11: Implement A.17/A.18 confidence verification interfaces

**Files:**
- Modify: `api/verify/archive_confidence.py`
- Modify: `api/verify/vehicle_archive_confidence.py`
- Create: `services/verify/archive_confidence.py`
- Create: `services/verify/vehicle_archive_confidence.py`
- Create: `tasks/verify/archive_confidence.py`
- Create: `tasks/verify/vehicle_archive_confidence.py`
- Modify: `services/__init__.py`
- Modify: `tasks/__init__.py`
- Test: `tests/api/test_archive_confidence_api.py`
- Test: `tests/api/test_vehicle_archive_confidence_api.py`

**Step 1: Write the failing tests**

```python
async def test_archive_confidence_contract(...):
    ...

async def test_vehicle_archive_confidence_contract(...):
    ...
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/api/test_archive_confidence_api.py tests/api/test_vehicle_archive_confidence_api.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

- Implement confidence verification logic and response status mapping.

**Step 4: Run test to verify it passes**

Run: `pytest tests/api/test_archive_confidence_api.py tests/api/test_vehicle_archive_confidence_api.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add api/verify/*.py services/verify/*.py tasks/verify/*.py services/__init__.py tasks/__init__.py tests/api/test_archive_confidence_api.py tests/api/test_vehicle_archive_confidence_api.py
git commit -m "feat: implement 2350 archive confidence interfaces"
```

### Task 12: Final verification and docs sync

**Files:**
- Modify: `.docs/ARCHITECTURE.md`
- Modify: `.docs/PROTOCOL_1400.md`
- Modify: `.docs/PROTOCOL_2350.md`
- Modify: `.docs/TESTING.md`

**Step 1: Add/refresh docs to match delivered behavior**

Include final route table, payload wrappers, and test strategy.

**Step 2: Run full test suite**

Run: `pytest -q`
Expected: PASS

**Step 3: Run migration verification**

Run: `alembic upgrade head`
Expected: SUCCESS with no migration error

**Step 4: Optional runtime smoke checks**

Run: `uvicorn main:app --host 0.0.0.0 --port 8000`
Expected: service starts and `/ready` returns success

**Step 5: Commit**

```bash
git add .docs/ARCHITECTURE.md .docs/PROTOCOL_1400.md .docs/PROTOCOL_2350.md .docs/TESTING.md
git commit -m "docs: sync architecture protocol and testing after 1400+2350 completion"
```
