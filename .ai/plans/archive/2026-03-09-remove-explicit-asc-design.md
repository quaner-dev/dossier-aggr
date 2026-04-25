# Remove Explicit ASC Design

**Goal:** Remove explicit `.asc()` usage from `face` and `person` list queries while preserving the existing ordering and fixed-size list behavior.

**Scope:** This change is limited to the repository list queries for `Face` and `Person`, plus repository-level tests that verify the generated SQL no longer contains explicit `ASC`.

**Decision:** Keep `order_by(...)` and `limit(100)` unchanged, but replace:

- `order_by(Face.FaceID.asc())` with `order_by(Face.FaceID)`
- `order_by(Person.PersonID.asc())` with `order_by(Person.PersonID)`

**Why this approach:** It is the smallest possible change that matches the request. It does not alter the public API, the returned data shape, or the existing pagination limit. It only removes redundant explicit ascending syntax.

**Validation:** Add repository tests that inspect the compiled statement text and assert it still contains `ORDER BY` and `LIMIT`, but no longer contains `ASC`.
