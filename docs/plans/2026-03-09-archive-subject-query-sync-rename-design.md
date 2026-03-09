# Archive Subject Query Sync Rename Design

**Goal:** Rename the internal archive subject query handler from `archive_subject_query_sync_read` to `archive_subject_query_sync` without changing the HTTP contract or runtime behavior.

**Scope**
- Modify only the handler name in `api/archive/archive_subject.py`.
- Update the direct test references in `tests/test_api_archive_subject.py`.
- Do not change the route path, request/response schema, or other `*_query_sync_read` handlers.

**Approaches**
1. Rename only this method and its direct tests.
   - Pros: minimal diff, matches the current request, no protocol impact.
   - Cons: other 2350 query handlers still keep the old suffix.
2. Rename the full `*_query_sync_read` family.
   - Pros: naming consistency across modules.
   - Cons: broader change than requested.

**Decision**
- Use approach 1.

**Behavior**
- Keep `POST {constants.ARCHIVE_SUBJECT_QUERY_SYNC_URL}` unchanged.
- Keep the returned `ArchiveSubjectQueryResultSchema` unchanged.
- Only change the Python function identifier and test references.

**Verification**
- Update the archive subject API test to reference `archive_subject_query_sync`.
- Run the targeted test to observe the expected import failure before implementation.
- Implement the rename.
- Re-run the targeted test, `compileall`, and `pytest -q`.
