# Taskiq Dispatch Typing Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make `dispatch_and_wait` type Taskiq-decorated async tasks as returning their awaited payload type instead of `Coroutine[..., T]`.

**Architecture:** Keep the runtime behavior unchanged and fix the typing at the shared dispatch helper boundary. The helper will accept either a direct Taskiq return type or a coroutine-wrapped Taskiq return type, then expose a single awaited payload type to callers.

**Tech Stack:** Python, Taskiq, pytest, typing

---

### Task 1: Lock the current runtime contract with a targeted test

**Files:**
- Modify: `tests/services/test_task_dispatch.py`
- Test: `tests/services/test_task_dispatch.py`

**Step 1: Write the failing test**

Add a focused test around an `async def` Taskiq task that returns a concrete payload and is passed through `dispatch_and_wait`.

**Step 2: Run test to verify it fails**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/services/test_task_dispatch.py -q`
Expected: FAIL if the new assertion or fixture setup is incomplete.

**Step 3: Write minimal implementation**

Update `services/task_dispatch.py` to express the Taskiq helper type in terms of the awaited payload type rather than the coroutine wrapper type.

**Step 4: Run test to verify it passes**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/services/test_task_dispatch.py -q`
Expected: PASS

**Step 5: Run broader verification**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest -q`
Expected: PASS or reveal unrelated existing failures.

**Step 6: Verify syntax**

Run: `source /root/dossier-aggr-venv/bin/activate && python -m compileall services/task_dispatch.py tests/services/test_task_dispatch.py`
Expected: PASS
