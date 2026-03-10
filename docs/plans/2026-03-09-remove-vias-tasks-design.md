# Remove VIAS Tasks Interface Design

**Goal:** Remove the unsupported `/VIAS/Tasks` interface chain so the service only exposes the protocol scope that is currently required.

**Scope**
- Remove `ARCHIVE_TASKS_URL` from `core/constants.py`.
- Remove the `/VIAS/Tasks` API router and its service/task/repository implementation chain.
- Remove route registration and aggregate exports that currently pull `ArchiveTask` runtime code into the app.
- Update tests that currently expect `/VIAS/Tasks` to exist.
- Update `.docs/ARCHITECTURE.md`, `.docs/PROTOCOL_2350.md`, and `.docs/TESTING.md` so they no longer claim the interface is implemented.

**Non-Goals**
- Do not remove the `ArchiveTask` data model or migration history unless required by imports.
- Do not alter any non-`VIAS` protocol endpoints.

**Approaches**
1. Full runtime removal.
   - Delete the `/VIAS/Tasks` API, service, task, and repository modules.
   - Remove imports and route registration.
   - Update tests and docs.
   - Pros: no dead runtime code, aligns with current protocol scope.
   - Cons: touches multiple aggregation files.
2. Hide only the route.
   - Remove router registration but keep the rest of the chain in place.
   - Pros: fewer file edits.
   - Cons: leaves dead code and misleading exports.

**Decision**
- Use approach 1.

**Verification**
- Update route tests to assert `/VIAS/Tasks` is absent.
- Remove or update unit tests that target the deleted API and layering chain.
- Run targeted tests for protocol routes and collection/archive layering.
- Run full `pytest -q`.
