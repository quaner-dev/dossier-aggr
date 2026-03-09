# Archive Library A.5 Protocol Correction Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make `ArchiveLibrary` fully follow A.5 table A.4 by using `/VIID/ArchiveLibraries` for batch query/create/update/delete only.

**Architecture:** The query path becomes a synchronous `api -> service -> repository` read on the collection resource. Batch delete remains a write path through `service -> task -> repository`. The incorrect query-sync constant and route are removed so the codebase reflects one protocol-correct contract instead of dual behavior.

**Tech Stack:** Python, FastAPI, SQLModel, Taskiq, pytest

---

### Task 1: Express the corrected contract in tests

**Files:**
- Modify: `tests/test_api_archive_library.py`
- Modify: `tests/services/test_collection_archive_layering.py`
- Modify: `tests/protocol/test_2350_routes.py`

**Step 1: Write the failing tests**

Update tests to expect:
- `archive_libraries_query`
- `archive_libraries_create`
- `archive_libraries_update`
- `archive_libraries_delete`
- no `ArchiveLibraryQuerySync` route
- `DELETE /VIID/ArchiveLibraries` uses `IDList`

**Step 2: Run test to verify it fails**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/test_api_archive_library.py tests/services/test_collection_archive_layering.py tests/protocol/test_2350_routes.py -q`
Expected: FAIL because the implementation still uses the wrong query route and old handler names.

**Step 3: Write minimal implementation**

Update the API/service/task/repository/constants code to match A.5.

**Step 4: Run tests to verify they pass**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/test_api_archive_library.py tests/services/test_collection_archive_layering.py tests/protocol/test_2350_routes.py -q`
Expected: PASS

**Step 5: Sync docs**

Update:
- `.docs/PROTOCOL_2350.md`
- `.docs/ARCHITECTURE.md`
- `.docs/TESTING.md`

**Step 6: Run broader verification**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest -q`
Expected: PASS

**Step 7: Verify syntax**

Run: `source /root/dossier-aggr-venv/bin/activate && python -m compileall api/library/archive_library.py services/library/archive_library.py tasks/library/archive_library.py repo/library/archive_library.py constants.py tests/test_api_archive_library.py tests/services/test_collection_archive_layering.py tests/protocol/test_2350_routes.py`
Expected: PASS
