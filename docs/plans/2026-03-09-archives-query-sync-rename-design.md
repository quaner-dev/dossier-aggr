# Archives Query Sync Rename Design

**Goal:** Rename the internal archive query route function from `archives_query_sync_read` to `archives_query_sync` without changing the HTTP contract or runtime behavior.

**Scope**
- Modify only the archive query handler in `api/archive/archives.py`.
- Update direct test references in `tests/test_api_archives.py`.
- Do not change the route path, request/response schema, or any other `*_query_sync_read` handlers.

**Approaches**
1. Rename only this method and its direct tests.
   - Pros: minimal diff, matches the current request, no protocol impact.
   - Cons: naming remains inconsistent with the other 2350 query handlers.
2. Rename the whole `*_query_sync_read` family.
   - Pros: consistent naming across modules.
   - Cons: broader change than requested and unnecessary for the current task.

**Decision**
- Use approach 1.

**Behavior**
- Keep `GET {constants.ARCHIVES_QUERY_SYNC_URL}` unchanged.
- Keep the returned `ArchiveQueryResultSchema` unchanged.
- Only change the Python function identifier and its test references.

**Verification**
- Update the archive API test to reference `archives_query_sync`.
- Run the targeted archive API tests to observe the expected failure before implementation.
- Implement the rename.
- Re-run the same targeted tests and `compileall` on the touched files.
