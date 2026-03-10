# ArchiveLibrary And VehicleArchive Protocol Correction Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make the `ArchiveLibrary` and `VehicleArchive` interfaces conform to GA/T 2350.5-2025 A.5, A.11, and A.12.

**Architecture:** `ArchiveLibrary` query becomes a collection `GET` on `/VIID/ArchiveLibraries`, with sync reads still going `api -> service -> repository`. `VehicleArchive` query becomes a protocol-style sync query `POST` on `/VIID/VehicleArchivesQuerySync`, carrying an `ArchiveQuerySchema` request and returning `ArchiveQueryResultSchema` with vehicle results. Batch deletes stay on the write path and adopt `IDList` at the API boundary.

**Tech Stack:** Python, FastAPI, SQLModel, Taskiq, pytest

---

### Task 1: Express the corrected contracts in tests

**Files:**
- Modify: `tests/test_api_archive_library.py`
- Modify: `tests/test_api_vehicle_archive.py`
- Modify: `tests/services/test_collection_archive_layering.py`
- Modify: `tests/protocol/test_2350_routes.py`

**Step 1: Write the failing tests**

Update tests to expect:
- `GET /VIID/ArchiveLibraries` query handler, no `ArchiveLibraryQuerySync`
- `DELETE /VIID/ArchiveLibraries` using `IDList`
- `POST /VIID/VehicleArchivesQuerySync` with `ArchiveQuerySchema`
- `ArchiveQueryResultSchema` containing `VehicleArchiveListObject`
- `DELETE /VIID/VehicleArchives` using `IDList`

**Step 2: Run test to verify it fails**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/test_api_archive_library.py tests/test_api_vehicle_archive.py tests/services/test_collection_archive_layering.py tests/protocol/test_2350_routes.py -q`
Expected: FAIL because the implementation still exposes the wrong contracts.

**Step 3: Write minimal implementation**

Update constants, API, service, repository, and result model code to match the protocol tables.

**Step 4: Run tests to verify they pass**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/test_api_archive_library.py tests/test_api_vehicle_archive.py tests/services/test_collection_archive_layering.py tests/protocol/test_2350_routes.py -q`
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

Run: `source /root/dossier-aggr-venv/bin/activate && python -m compileall core/constants.py api/library/archive_library.py api/vehicle/vehicle_archive.py services/library/archive_library.py services/vehicle/vehicle_archive.py repo/library/archive_library.py repo/vehicle/vehicle_archive.py models/archive/archive_query_result.py models/__init__.py tests/test_api_archive_library.py tests/test_api_vehicle_archive.py tests/services/test_collection_archive_layering.py tests/protocol/test_2350_routes.py`
Expected: PASS
