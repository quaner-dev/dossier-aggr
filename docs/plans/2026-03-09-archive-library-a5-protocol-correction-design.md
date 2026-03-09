# Archive Library A.5 Protocol Correction Design

**Goal:** Correct the `ArchiveLibrary` API so it matches GA/T 2350.5-2025 A.5 table A.4: batch create, query, update, and delete all use `/VIID/ArchiveLibraries`.

**Scope**
- Modify `api/library/archive_library.py`, `services/library/archive_library.py`, `tasks/library/archive_library.py`, `repositories/library/archive_library.py`, and `constants.py`.
- Update tests in `tests/test_api_archive_library.py`, `tests/services/test_collection_archive_layering.py`, and `tests/protocol/test_2350_routes.py`.
- Update `.docs/PROTOCOL_2350.md`, `.docs/ARCHITECTURE.md`, and `.docs/TESTING.md`.

**Approaches**
1. Strict replacement: remove `/VIID/ArchiveLibraryQuerySync` and move query onto `GET /VIID/ArchiveLibraries`, with query-string attribute filters and `IDList` batch delete.
   - Pros: matches the protocol table exactly and removes the incorrect extra route.
   - Cons: requires touching several layers and tests.
2. Compatibility mode: keep the old query-sync route and add the correct route beside it.
   - Pros: lower compatibility risk for existing callers.
   - Cons: leaves a protocol-wrong route in the codebase and violates the “strictly follow protocol” requirement.

**Decision**
- Use approach 1.

**Behavior**
- Remove `ARCHIVE_LIBRARY_QUERY_SYNC_URL` and its route.
- Add `GET /VIID/ArchiveLibraries` returning `ArchiveLibraryListSchema`.
- Support top-level `ArchiveLibrary` attribute filters from query-string key/value pairs.
- Keep `POST` and `PUT` on `/VIID/ArchiveLibraries`.
- Keep `DELETE /VIID/ArchiveLibraries`, but use protocol key `IDList`.

**Verification**
- Update the API, layering, and route tests first to the target contract.
- Run the targeted tests to observe failures before implementation.
- Implement the minimal code changes.
- Re-run targeted tests, `compileall`, and the full `pytest -q` suite.
