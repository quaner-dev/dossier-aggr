# Fix Update Faces Task Test Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make the `update_faces_task` delegation test reflect the real repository call signature so the suite passes again.

**Architecture:** This is a test-only correction. The task already delegates correctly using a keyword argument, so the test double must accept the same keyword name. No production code changes are required.

**Tech Stack:** Python, pytest, monkeypatch

---

### Task 1: Align the fake repository signature with the task call

**Files:**
- Modify: `tests/tasks/test_delete_tasks.py`
- Test: `tests/tasks/test_delete_tasks.py`

**Step 1: Write the failing test**

Use the existing failing test `test_update_faces_task_delegates_to_repository` as the red state.

**Step 2: Run test to verify it fails**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/tasks/test_delete_tasks.py::test_update_faces_task_delegates_to_repository -q`
Expected: FAIL with `unexpected keyword argument 'faces'`

**Step 3: Write minimal implementation**

Change the fake function parameter from `faces_param` to `faces` and keep the assertions on the same list contents.

**Step 4: Run test to verify it passes**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/tasks/test_delete_tasks.py::test_update_faces_task_delegates_to_repository -q`
Expected: PASS

**Step 5: Run broader verification**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest -q`
Expected: PASS or reveal unrelated failures.

**Step 6: Verify syntax**

Run: `source /root/dossier-aggr-venv/bin/activate && python -m compileall tests/tasks/test_delete_tasks.py`
Expected: PASS
