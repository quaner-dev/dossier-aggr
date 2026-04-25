# Repositories To Repo Rename Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace the runtime package name `repositories` with `repo` everywhere the codebase depends on it.

**Architecture:** The change is a package-level rename only. Runtime code, tests, and docs should all point at `repo/...` for persistence-layer modules, while `tests/repositories/` stays in place because it is a test suite path rather than the runtime package.

**Tech Stack:** Python, FastAPI, SQLModel, pytest, Ruff

---

### Task 1: Rename the runtime package and fix imports

**Files:**
- Move: `repo/` -> `repo/`
- Modify: all Python files importing `repositories...`

**Step 1: Write the failing check**

Use a search to identify all current `repositories...` imports.

**Step 2: Run check to verify old references exist**

Run: `rg -n "\bfrom repositories\b|\bimport repositories\b|repo/" .`
Expected: multiple matches across services, tasks, tests, and docs.

**Step 3: Write minimal implementation**

Move the package directory and update imports from `repositories...` to `repo...`.

**Step 4: Run verification search**

Run: `rg -n "\bfrom repositories\b|\bimport repositories\b" .`
Expected: no matches in runtime code or tests.

### Task 2: Update docs and broader references

**Files:**
- Modify: `.ai/project/README.md`
- Modify: `.ai/testing/README.md`
- Modify: `.ai/plans/archive/*.md` entries that refer to the runtime package path

**Step 1: Update docs**

Replace `repo/...` path mentions with `repo/...` when they describe the runtime package.

**Step 2: Run tests and lint**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest -q`
Expected: PASS

Run: `source /root/dossier-aggr-venv/bin/activate && ruff check .`
Expected: PASS
