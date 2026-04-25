# Person API Naming Design

**Goal:** Align the `person` API route function names with the existing `face` API naming style by placing the noun before the verb.

**Scope:** This change is limited to the API module and direct API unit tests. It does not change URLs, request or response schemas, service names, task names, repository names, or protocol docs.

**Decision:** Rename the route functions in [api/person/person.py](/root/dossier-aggr/api/person/person.py) from verb-first names to noun-first names:

- `list_persons` -> `persons_query`
- `create_persons` -> `persons_create`
- `update_persons` -> `persons_update`
- `delete_persons` -> `persons_delete`
- `get_person` -> `person_query`

**Why this approach:** It matches the naming pattern already used in [api/face/face.py](/root/dossier-aggr/api/face/face.py), keeps the public HTTP contract unchanged, and minimizes regression risk by limiting the change to function symbols and test imports.

**Validation:** Update direct imports in [tests/test_api_person.py](/root/dossier-aggr/tests/test_api_person.py) and run focused tests for that module. If the environment still lacks `pytest`, fall back to `python -m compileall` for syntax verification and report the test limitation explicitly.
