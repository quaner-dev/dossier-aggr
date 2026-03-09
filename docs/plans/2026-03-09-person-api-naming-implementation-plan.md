# Person API Naming Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rename `person` API route functions to noun-first names so the module matches the `face` API naming style.

**Architecture:** Keep the HTTP contract stable and only rename Python function symbols in the API layer. Update the direct API unit test imports and assertions to reference the new names. Do not change service, task, repository, or protocol behavior.

**Tech Stack:** FastAPI, SQLModel, pytest

---

### Task 1: Rename direct API test imports first

**Files:**
- Modify: `tests/test_api_person.py`
- Modify: `api/person/person.py`

**Step 1: Write the failing test**

Update the imports and direct function calls in `tests/test_api_person.py` so they reference:

```python
from api.person.person import (
    persons_query,
    persons_create,
    persons_update,
    persons_delete,
    person_query,
)
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_api_person.py -q`
Expected: FAIL because the renamed API functions do not exist yet.

**Step 3: Write minimal implementation**

Rename the route function definitions in `api/person/person.py` to:

```python
async def persons_query(...):
async def persons_create(...):
async def persons_update(...):
async def persons_delete(...):
async def person_query(...):
```

Do not change route decorators or business logic.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_api_person.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/test_api_person.py api/person/person.py docs/plans/2026-03-09-person-api-naming-design.md docs/plans/2026-03-09-person-api-naming-implementation-plan.md
git commit -m "refactor: align person api function naming"
```

### Task 2: Verify no direct references remain

**Files:**
- Modify: `tests/test_api_person.py`
- Verify: `api/person/person.py`

**Step 1: Write the failing test**

No new test code is required. The regression check is that no direct import or call site still expects the old API function names.

**Step 2: Run test to verify it fails**

Run: `rg -n "from api\\.person\\.person import|list_persons\\(|create_persons\\(|update_persons\\(|delete_persons\\(|get_person\\(" tests api`
Expected: only service calls and internal service method names remain; no direct API test imports use the old route function names.

**Step 3: Write minimal implementation**

If any stale direct API references remain, rename them to the new symbols.

**Step 4: Run test to verify it passes**

Run: `python -m compileall api/person/person.py tests/test_api_person.py`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/test_api_person.py api/person/person.py
git commit -m "test: update person api naming references"
```
