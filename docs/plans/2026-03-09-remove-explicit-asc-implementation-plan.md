# Remove Explicit ASC Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Remove explicit `.asc()` from `face` and `person` list repository queries without changing query semantics.

**Architecture:** Update only the repository query builders and verify the resulting SQL shape with repository-level tests. Keep ordering fields and `limit(100)` intact.

**Tech Stack:** SQLModel, pytest

---

### Task 1: Add failing repository tests

**Files:**
- Modify: `tests/repositories/test_person_face_delete_repositories.py`
- Modify: `repositories/face/face.py`
- Modify: `repositories/person/person.py`

**Step 1: Write the failing test**

Add assertions that the compiled list statements:

- contain `ORDER BY`
- contain the identifier column (`PersonID` / `FaceID`)
- contain `LIMIT`
- do **not** contain `ASC`

**Step 2: Run test to verify it fails**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/repositories/test_person_face_delete_repositories.py -q`
Expected: FAIL because the current SQL still contains explicit `ASC`.

**Step 3: Write minimal implementation**

Update the repository queries to use `order_by(Person.PersonID)` and `order_by(Face.FaceID)`.

**Step 4: Run test to verify it passes**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/repositories/test_person_face_delete_repositories.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/repositories/test_person_face_delete_repositories.py repositories/face/face.py repositories/person/person.py docs/plans/2026-03-09-remove-explicit-asc-design.md docs/plans/2026-03-09-remove-explicit-asc-implementation-plan.md
git commit -m "refactor: remove explicit asc from person and face lists"
```
