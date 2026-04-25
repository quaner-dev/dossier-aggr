# APE APS API Naming Align Design

**Goal:** Align the `ape` and `aps` API handler names with the `face` and `person` API naming style.

**Scope**
- Modify API handler names in `api/collection/ape.py` and `api/collection/aps.py`.
- Update direct test imports and invocations in `tests/test_api_ape.py` and `tests/test_api_aps.py`.
- Do not change URLs, request/response models, or runtime behavior.
- Do not rename service/task/repository methods, because they already follow the same layer pattern used by `face` and `person`.

**Approaches**
1. Rename only the API handlers and direct tests.
   - Pros: minimal diff, matches the `face/person` API surface naming, no behavior change.
   - Cons: internal service/repo names remain verb-first, but that is already how `face/person` are organized.
2. Rename all layers to noun-first names.
   - Pros: full noun-first naming everywhere.
   - Cons: would diverge from the existing `face/person` service/task/repository conventions and create unnecessary churn.

**Decision**
- Use approach 1.

**Naming**
- `list_apes` -> `apes_query`
- `update_apes` -> `apes_update`
- `list_aps` -> `apss_query`

**Verification**
- Update the API tests to import and call the new handler names.
- Run the targeted API tests first to observe the expected import failure before implementation.
- Rename the handlers.
- Re-run targeted tests, `compileall`, and the full `pytest -q` suite.
