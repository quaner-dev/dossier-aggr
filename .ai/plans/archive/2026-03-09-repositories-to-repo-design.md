# Repositories To Repo Rename Design

**Goal:** Rename the runtime persistence package from `repo/` to `repo/` and keep code, tests, and documentation references consistent.

**Scope**
- Rename the top-level runtime package directory from `repo/` to `repo/`.
- Update all Python imports from `repositories...` to `repo...`.
- Update `.ai/` and `.ai/plans/archive/` path references from `repo/...` to `repo/...` where they refer to the runtime package.
- Update test imports and path mentions that reference the runtime package.

**Non-Goals**
- Do not rename the `tests/repositories/` directory in this change.
- Do not change repository function names, API behavior, or database logic.

**Approaches**
1. Strict rename without compatibility layer.
   - Move `repo/` to `repo/`.
   - Update all imports and path references.
   - Pros: one final name, no alias package to maintain.
   - Cons: touches many files at once.
2. Add `repo/` and keep `repo/` as a forwarding alias.
   - Pros: lower short-term import risk.
   - Cons: leaves two names in the codebase and defeats the cleanup.

**Decision**
- Use approach 1.

**Verification**
- Search for stale `repositories.` and `repo/` references after the rename.
- Run `pytest -q`.
- Run `ruff check .`.
