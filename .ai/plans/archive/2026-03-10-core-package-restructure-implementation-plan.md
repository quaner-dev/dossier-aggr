# Core Package Restructure Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Consolidate root-level infrastructure modules into `core/` without changing application behavior.

**Architecture:** `main.py` remains the root entrypoint, but all shared runtime infrastructure moves into `core/`. Runtime code, tests, docs, and worker startup strings must all point at `core.*` so the project has a single consistent import path for infrastructure concerns.

**Tech Stack:** Python, FastAPI, SQLModel, Taskiq, pytest, Ruff

---

### Task 1: Lock the intended project layout in a failing test

**Files:**
- Create: `tests/test_project_layout.py`

**Step 1: Write the failing test**

Add a test asserting:
- `main.py` still exists at the root
- `core/settings.py`, `core/database.py`, `core/constants.py`, `core/exceptions.py`, `core/utils.py`, `core/auth.py`, and `core/brokers.py` exist
- the old root-level infrastructure files no longer exist

**Step 2: Run test to verify it fails**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/test_project_layout.py -q`
Expected: FAIL because the files are still at the root.

**Step 3: Write minimal implementation**

Move the files under `core/` and update imports.

**Step 4: Run test to verify it passes**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/test_project_layout.py -q`
Expected: PASS

### Task 2: Update startup/config/doc references

**Files:**
- Modify: `README.md`
- Modify: `AGENTS.md`
- Modify: `dossier-aggr/values.yaml`
- Modify: `.ai/project/README.md`
- Modify: any code/tests/docs that still import or mention root infrastructure modules

**Step 1: Update runtime/documentation references**

Replace root imports with `core.*` and update `brokers:broker` to `core.brokers:broker` where it is required for runtime startup.

**Step 2: Run full verification**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest -q`
Expected: PASS

Run: `source /root/dossier-aggr-venv/bin/activate && ruff check .`
Expected: PASS
