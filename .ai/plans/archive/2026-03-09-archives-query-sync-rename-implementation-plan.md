# Archives Query Sync Rename Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rename the internal archive query handler to `archives_query_sync` while preserving the existing HTTP behavior.

**Architecture:** This is an internal naming refactor only. The FastAPI route decorator remains bound to the same path and schema, so the runtime API contract does not move. The only required downstream change is the direct unit test import and assertion entry point.

**Tech Stack:** Python, FastAPI, pytest

---

### Task 1: Rename the archive query test entry point

**Files:**
- Modify: `tests/test_api_archives.py`
- Test: `tests/test_api_archives.py`

**Step 1: Write the failing test**

Change the import and the query test call from `archives_query_sync_read` to `archives_query_sync`.

**Step 2: Run test to verify it fails**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/test_api_archives.py -q`
Expected: FAIL with an import error because `archives_query_sync` is not defined yet.

**Step 3: Write minimal implementation**

Rename the function in `api/archive/archives.py` from `archives_query_sync_read` to `archives_query_sync`.

**Step 4: Run test to verify it passes**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/test_api_archives.py -q`
Expected: PASS

**Step 5: Verify syntax**

Run: `source /root/dossier-aggr-venv/bin/activate && python -m compileall api/archive/archives.py tests/test_api_archives.py`
Expected: PASS
