# ArchiveLibrary And VehicleArchive Protocol Correction Design

**Goal:** Correct the `ArchiveLibrary` and `VehicleArchive` interfaces so they match GA/T 2350.5-2025 A.5, A.11, and A.12 exactly enough for this codebase.

**Scope**
- Modify `core/constants.py`.
- Modify `api/library/archive_library.py` and `api/vehicle/vehicle_archive.py`.
- Modify `services/library/archive_library.py` and `services/vehicle/vehicle_archive.py`.
- Modify `repo/library/archive_library.py` and `repo/vehicle/vehicle_archive.py`.
- Modify `models/archive/archive_query_result.py` and `models/__init__.py`.
- Update tests in `tests/test_api_archive_library.py`, `tests/test_api_vehicle_archive.py`, `tests/services/test_collection_archive_layering.py`, and `tests/protocol/test_2350_routes.py`.
- Update `.docs/PROTOCOL_2350.md`, `.docs/ARCHITECTURE.md`, and `.docs/TESTING.md`.

**Protocol Basis**
- A.5 / Table A.4: `/VIID/ArchiveLibraries` handles batch `POST/GET/PUT/DELETE`.
- A.11 / Table A.10: `/VIID/VehicleArchivesQuerySync` is a `POST` query endpoint with `<ArchiveQuery>` request and `<ArchiveQueryResult>` response.
- A.12 / Table A.11: `/VIID/VehicleArchives` handles batch `POST/PUT/DELETE`, with delete key `IDList`.

**Approaches**
1. Strict correction.
   - Remove the wrong `ArchiveLibraryQuerySync` route.
   - Move archive-library query onto `GET /VIID/ArchiveLibraries`.
   - Convert vehicle-archive query to `POST /VIID/VehicleArchivesQuerySync` with `ArchiveQuerySchema` and `ArchiveQueryResultSchema`.
   - Use protocol delete key `IDList` for both collection deletes.
   - Pros: matches the protocol tables and removes wrong contracts.
   - Cons: requires coordinated updates across API, service, repository, tests, and docs.
2. Compatibility layering.
   - Keep the wrong routes and add correct ones beside them.
   - Pros: lower risk for any hidden local caller.
   - Cons: leaves protocol-wrong behavior in place and conflicts with the requirement to strictly follow the protocol.

**Decision**
- Use approach 1.

**Behavior**
- `ArchiveLibrary`
  - `GET /VIID/ArchiveLibraries` returns `ArchiveLibraryListSchema`.
  - Query-string filters map to top-level `ArchiveLibrary` attributes.
  - `DELETE /VIID/ArchiveLibraries` uses `IDList`.
- `VehicleArchive`
  - `POST /VIID/VehicleArchivesQuerySync` accepts `ArchiveQuerySchema`.
  - It returns `ArchiveQueryResultSchema` with `VehicleArchiveListObject`.
  - Filtering uses `ArchiveQuery.Fields` where supported.
  - `DELETE /VIID/VehicleArchives` uses `IDList`.

**Verification**
- Update the affected API, layering, and route tests first.
- Run those targeted tests to observe failures before implementation.
- Implement the minimal code changes.
- Re-run targeted tests, `compileall`, and the full `pytest -q` suite.
