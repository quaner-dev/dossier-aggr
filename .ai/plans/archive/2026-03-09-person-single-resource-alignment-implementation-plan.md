# Person Single Resource Alignment Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add single-person update and delete endpoints so the `person` API matches the `face` API organization and protocol contract.

**Architecture:** Extend the API layer only where missing. Reuse the existing `PersonService.update_person` and `PersonService.delete_person` methods, and mirror the success response shape already used by `face` single-resource routes. Keep batch and single-resource routes explicitly separate.

**Tech Stack:** FastAPI, SQLModel, pytest

---

### Task 1: Add failing direct API tests for single-person update/delete

**Files:**
- Modify: `tests/test_api_person.py`
- Modify: `api/person/person.py`

**Step 1: Write the failing test**

Add imports and a new test in `tests/test_api_person.py` that expects:

```python
from api.person.person import person_update, person_delete
```

and verifies:

```python
res = await person_update(person_id="P-001", data=payload, service=...)
assert res.StatusCode == "0"
assert res.Id == "P-001"
```

**Step 2: Run test to verify it fails**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/test_api_person.py -q`
Expected: FAIL because `person_update` and `person_delete` do not exist yet.

**Step 3: Write minimal implementation**

Add `person_update` and `person_delete` handlers in `api/person/person.py`, mirroring the pattern used by `face` single-resource routes.

**Step 4: Run test to verify it passes**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/test_api_person.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/test_api_person.py api/person/person.py
git commit -m "feat: add single person update and delete routes"
```

### Task 2: Add HTTP contract and OpenAPI regression coverage

**Files:**
- Modify: `tests/protocol/test_api_http_contracts.py`
- Modify: `tests/protocol/test_1400_routes.py`
- Modify: `api/person/person.py`

**Step 1: Write the failing test**

Extend the HTTP contract test to call:

```python
await client.put("/VIID/Persons/P-HTTP-001", json=payload)
await client.delete("/VIID/Persons/P-HTTP-001")
```

Extend the route registration test to require:

```python
assert "put" in paths["/VIID/Persons/{person_id}"]
assert "delete" in paths["/VIID/Persons/{person_id}"]
```

**Step 2: Run test to verify it fails**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/protocol/test_api_http_contracts.py tests/protocol/test_1400_routes.py -q`
Expected: FAIL because the routes are not registered yet.

**Step 3: Write minimal implementation**

Keep the handlers registered in `api/person/person.py` and adjust the fake service in the HTTP test to support `update_person` and `delete_person`.

**Step 4: Run test to verify it passes**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/protocol/test_api_http_contracts.py tests/protocol/test_1400_routes.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/protocol/test_api_http_contracts.py tests/protocol/test_1400_routes.py api/person/person.py
git commit -m "test: cover single person resource routes"
```

### Task 3: Sync protocol documentation

**Files:**
- Modify: `.ai/protocols/1400/README.md`
- Modify: `.ai/project/README.md`
- Modify: `.ai/testing/README.md`

**Step 1: Write the failing test**

No new automated test is needed. The regression is doc drift: `person` docs currently only describe single-person query.

**Step 2: Run test to verify it fails**

Manually inspect the docs and confirm they do not mention single-person `PUT/DELETE`.

**Step 3: Write minimal implementation**

Update the docs so `person` matches the `face` documentation style:

- `PROTOCOL_1400.md`: add single-person `PUT/DELETE`
- `ARCHITECTURE.md`: note batch/single split
- `TESTING.md`: add single-person update/delete rows

**Step 4: Run test to verify it passes**

Run: `python -m compileall api/person/person.py tests/test_api_person.py tests/protocol/test_api_http_contracts.py tests/protocol/test_1400_routes.py`
Expected: PASS

**Step 5: Commit**

```bash
git add .ai/protocols/1400/README.md .ai/project/README.md .ai/testing/README.md
git commit -m "docs: sync person single-resource contract"
```
