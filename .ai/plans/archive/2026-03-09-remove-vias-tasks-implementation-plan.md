# Remove VIAS Tasks Interface Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Delete the unsupported `/VIAS/Tasks` runtime interface and all associated exports, tests, and implementation claims.

**Architecture:** The app should stop importing or registering the `ArchiveTask` API chain entirely. `ArchiveTask` persistence artifacts can remain on disk if they are not part of the runtime interface, but the FastAPI router, service facade, Taskiq tasks, repository facade, and aggregate exports should be removed so OpenAPI no longer exposes `/VIAS/Tasks`.

**Tech Stack:** Python, FastAPI, SQLModel, Taskiq, pytest

---

### Task 1: Express the removal in tests

**Files:**
- Modify: `tests/protocol/test_2350_routes.py`
- Modify: `tests/services/test_collection_archive_layering.py`
- Delete: `tests/test_api_archive_task.py`

**Step 1: Write the failing test**

Update the protocol route test to assert `/VIAS/Tasks` is not present in OpenAPI.

**Step 2: Run test to verify it fails**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/protocol/test_2350_routes.py -q`
Expected: FAIL because the route is still registered.

**Step 3: Write minimal implementation**

Remove the constant, router, imports, aggregate exports, and archive-task runtime modules.

**Step 4: Run tests to verify they pass**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/protocol/test_2350_routes.py tests/services/test_collection_archive_layering.py -q`
Expected: PASS

### Task 2: Sync docs and run broader verification

**Files:**
- Modify: `.ai/protocols/2350/README.md`
- Modify: `.ai/project/README.md`
- Modify: `.ai/testing/README.md`

**Step 1: Update docs**

Mark A.6 as intentionally not implemented in the current service scope and remove any architecture/testing claims that `/VIAS/Tasks` is active.

**Step 2: Run broader verification**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest -q`
Expected: PASS
