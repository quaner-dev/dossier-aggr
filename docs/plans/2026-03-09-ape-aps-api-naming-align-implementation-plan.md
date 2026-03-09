# APE APS API Naming Align Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rename the `ape` and `aps` API handlers so they match the `face/person` API naming style without changing behavior.

**Architecture:** This is an internal API handler naming refactor. The FastAPI decorators keep the same paths and schemas, so the HTTP contract does not move. Only direct imports in API unit tests need to change.

**Tech Stack:** Python, FastAPI, pytest

---

### Task 1: Express the new API names in tests

**Files:**
- Modify: `tests/test_api_ape.py`
- Modify: `tests/test_api_aps.py`
- Test: `tests/test_api_ape.py`
- Test: `tests/test_api_aps.py`

**Step 1: Write the failing tests**

Change the imports and calls:
- `list_apes` -> `apes_query`
- `update_apes` -> `apes_update`
- `list_aps` -> `apss_query`

**Step 2: Run test to verify it fails**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/test_api_ape.py tests/test_api_aps.py -q`
Expected: FAIL with import errors because the renamed handlers do not exist yet.

**Step 3: Write minimal implementation**

Rename the handlers in:
- `api/collection/ape.py`
- `api/collection/aps.py`

**Step 4: Run test to verify it passes**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/test_api_ape.py tests/test_api_aps.py -q`
Expected: PASS

**Step 5: Verify syntax**

Run: `source /root/dossier-aggr-venv/bin/activate && python -m compileall api/collection/ape.py api/collection/aps.py tests/test_api_ape.py tests/test_api_aps.py`
Expected: PASS

**Step 6: Run broader verification**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest -q`
Expected: PASS
