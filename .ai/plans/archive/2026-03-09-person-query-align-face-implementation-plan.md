# Person Query Align Face Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Change `GET /VIID/Persons` so it matches `GET /VIID/Faces`: return the default fixed-size list directly, without filter parameters.

**Architecture:** Remove filtering from the API layer and move list sizing into the repository layer. Keep `PersonService.list_persons()` as a thin pass-through to the repository so the behavior stays consistent with `FaceService.list_faces()`.

**Tech Stack:** FastAPI, SQLModel, pytest

---

### Task 1: Write the failing HTTP contract regression

**Files:**
- Modify: `tests/protocol/test_api_http_contracts.py`
- Modify: `api/person/person.py`

**Step 1: Write the failing test**

Change the person query assertion so the request still sends `person_ids=P-HTTP-002`, but now expects the full default list:

```python
person_res = await client.get("/VIID/Persons", params={"person_ids": "P-HTTP-002"})
assert len(person_items) == 2
assert person_items[0]["PersonID"] == "P-HTTP-001"
```

**Step 2: Run test to verify it fails**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/protocol/test_api_http_contracts.py -q`
Expected: FAIL because the current API still filters the list.

**Step 3: Write minimal implementation**

Remove the query parameters and filter branches from `persons_query` in `api/person/person.py`.

**Step 4: Run test to verify it passes**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/protocol/test_api_http_contracts.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/protocol/test_api_http_contracts.py api/person/person.py
git commit -m "refactor: align person query api with face"
```

### Task 2: Align repository list behavior with face

**Files:**
- Modify: `repo/person/person.py`
- Test: `tests/services/test_person_face_layering.py`

**Step 1: Write the failing test**

Add a regression that expects `list_persons_repo` semantics to match `face`: fixed-size ordered list behavior, not "all rows or not found".

**Step 2: Run test to verify it fails**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/services/test_person_face_layering.py -q`
Expected: FAIL if the new expectation is asserted against the current repository behavior.

**Step 3: Write minimal implementation**

Update `repo/person/person.py` to:

- define `_DEFAULT_PERSON_LIST_LIMIT = 100`
- use `select(Person).order_by(Person.PersonID.asc()).limit(_DEFAULT_PERSON_LIST_LIMIT)`
- return the resulting list directly without raising `DataNotFoundError` on empty result

**Step 4: Run test to verify it passes**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/services/test_person_face_layering.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add repo/person/person.py tests/services/test_person_face_layering.py
git commit -m "refactor: limit person list query results"
```

### Task 3: Sync documentation and run focused verification

**Files:**
- Modify: `.ai/protocols/1400/README.md`
- Modify: `.ai/testing/README.md`
- Modify: `.ai/project/README.md`

**Step 1: Write the failing test**

No automated doc test is required. The failure condition is manual drift: docs still mention person query filters.

**Step 2: Run test to verify it fails**

Inspect the docs and confirm they still describe `person_ids` / `source_id` / `device_id` filtering.

**Step 3: Write minimal implementation**

Update docs so `GET /VIID/Persons` is described as returning the default top list, matching `face`.

**Step 4: Run test to verify it passes**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/test_api_person.py tests/protocol/test_api_http_contracts.py -q`

Run: `source /root/dossier-aggr-venv/bin/activate && python -m compileall api/person/person.py repo/person/person.py tests/protocol/test_api_http_contracts.py`

Expected: PASS

**Step 5: Commit**

```bash
git add .ai/protocols/1400/README.md .ai/testing/README.md .ai/project/README.md
git commit -m "docs: sync person query contract with face"
```
