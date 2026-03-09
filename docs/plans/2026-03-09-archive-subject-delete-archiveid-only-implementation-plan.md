# Archive Subject Delete ArchiveID Only Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make `ArchiveSubject` deletion operate only on `ArchiveID` across API, service, task, and repository.

**Architecture:** This change removes unused multi-filter delete semantics and collapses the delete path to a single required identifier. The API surface, service/task signatures, and repository implementation all become simpler and aligned with the desired contract. Test cleanup logic uses explicit known IDs instead of a broad delete-all shortcut.

**Tech Stack:** Python, FastAPI, SQLModel, Taskiq, pytest

---

### Task 1: Express the new delete contract in tests

**Files:**
- Modify: `tests/test_api_archive_subject.py`
- Modify: `tests/services/test_subject_verify_layering.py`
- Modify: `tests/e2e/test_async_eventual_consistency.py`

**Step 1: Write the failing tests**

Update the archive subject API/unit/layering/e2e tests so they call delete with only `archive_id`.

**Step 2: Run test to verify it fails**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/test_api_archive_subject.py tests/services/test_subject_verify_layering.py tests/e2e/test_async_eventual_consistency.py -q`
Expected: FAIL because the implementation still expects the removed parameters.

**Step 3: Write minimal implementation**

Update API/service/task/repository delete signatures and logic to use only `archive_id`.

**Step 4: Run tests to verify they pass**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/test_api_archive_subject.py tests/services/test_subject_verify_layering.py tests/e2e/test_async_eventual_consistency.py -q`
Expected: PASS or skip the e2e test per environment markers.

**Step 5: Sync docs**

Update `.docs/PROTOCOL_2350.md`, `.docs/ARCHITECTURE.md`, and `.docs/TESTING.md` to document ArchiveSubject delete-by-ArchiveID only behavior.

**Step 6: Run broader verification**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest -q`
Expected: PASS

**Step 7: Verify syntax**

Run: `source /root/dossier-aggr-venv/bin/activate && python -m compileall api/archive/archive_subject.py services/archive/archive_subject.py tasks/archive/archive_subject.py repositories/archive/archive_subject.py tests/test_api_archive_subject.py tests/services/test_subject_verify_layering.py tests/e2e/test_async_eventual_consistency.py`
Expected: PASS
