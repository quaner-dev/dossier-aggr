# Archive Subject Query Sync Rename Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rename the internal archive subject query handler to `archive_subject_query_sync` while preserving the existing HTTP behavior.

**Architecture:** This is an internal naming refactor only. The FastAPI route decorator remains bound to the same path and schema, so the runtime API contract does not change. The only required downstream change is the direct unit test import and invocation.

**Tech Stack:** Python, FastAPI, pytest

---

### Task 1: Rename the archive subject query test entry point

**Files:**
- Modify: `tests/test_api_archive_subject.py`
- Test: `tests/test_api_archive_subject.py`

**Step 1: Write the failing test**

Change the import and the query test call from `archive_subject_query_sync_read` to `archive_subject_query_sync`.

**Step 2: Run test to verify it fails**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/test_api_archive_subject.py -q`
Expected: FAIL with an import error because `archive_subject_query_sync` is not defined yet.

**Step 3: Write minimal implementation**

Rename the function in `api/archive/archive_subject.py` from `archive_subject_query_sync_read` to `archive_subject_query_sync`.

**Step 4: Run test to verify it passes**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/test_api_archive_subject.py -q`
Expected: PASS

**Step 5: Run broader verification**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest -q`
Expected: PASS or reveal unrelated failures.

**Step 6: Verify syntax**

Run: `source /root/dossier-aggr-venv/bin/activate && python -m compileall api/archive/archive_subject.py tests/test_api_archive_subject.py`
Expected: PASS
