# Core Package Restructure Design

**Goal:** Move root-level infrastructure modules into a dedicated `core/` package so the repository root only keeps entrypoint-level files.

**Scope**
- Move `auth.py`, `brokers.py`, `constants.py`, `database.py`, `exceptions.py`, `settings.py`, and `utils.py` into `core/`.
- Update all runtime imports to `core.*`.
- Update tests and documentation that reference those modules.
- Update worker startup references from `brokers:broker` to `core.brokers:broker` where required.

**Non-Goals**
- Do not move `main.py` out of the root.
- Do not change domain package structure under `api/`, `services/`, `tasks/`, `models/`, or `repo/`.
- Do not change application behavior beyond import paths and startup wiring.

**Approaches**
1. Full `core/` consolidation, recommended.
   - Move all root infrastructure modules in one pass.
   - Keep `main.py` at root.
   - Update imports, docs, and worker command references.
   - Pros: clean end state, no mixed structure.
   - Cons: broad import churn.
2. Partial move.
   - Move only `settings/database/constants/exceptions` first.
   - Keep `brokers/utils/auth` in root temporarily.
   - Pros: smaller diff.
   - Cons: leaves half-finished structure.
3. Deeper split (`core/`, `infra/`, `shared/`).
   - Pros: more granular taxonomy.
   - Cons: over-designed for current codebase.

**Decision**
- Use approach 1.

**Design**
- Create `core/` as a Python package.
- Move these files to `core/`:
  - `core/auth.py`
  - `core/brokers.py`
  - `core/constants.py`
  - `core/database.py`
  - `core/exceptions.py`
  - `core/settings.py`
  - `core/utils.py`
- Update imports across runtime code, tests, and docs.
- Keep deployment/config updates limited to startup strings that would otherwise break, specifically `brokers:broker` -> `core.brokers:broker`.

**Verification**
- Add a layout-level test proving the root infrastructure files moved under `core/`.
- Run the new layout test and watch it fail before the move.
- Run `pytest -q` after the refactor.
- Run `ruff check .` after the refactor.
