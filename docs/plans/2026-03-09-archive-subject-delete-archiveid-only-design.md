# Archive Subject Delete ArchiveID Only Design

**Goal:** Restrict the `ArchiveSubject` delete path to delete only by `ArchiveID`, removing support for the other legacy filter parameters across the full chain.

**Scope**
- Modify `api/archive/archive_subject.py`, `services/archive/archive_subject.py`, `tasks/archive/archive_subject.py`, and `repo/archive/archive_subject.py`.
- Update affected tests in `tests/test_api_archive_subject.py`, `tests/services/test_subject_verify_layering.py`, and `tests/e2e/test_async_eventual_consistency.py`.
- Update `.docs/PROTOCOL_2350.md`, `.docs/ARCHITECTURE.md`, and `.docs/TESTING.md`.

**Approaches**
1. Restrict only the API layer and keep lower layers backward compatible.
   - Pros: smaller internal diff.
   - Cons: leaves dead parameters and duplicate semantics in service/task/repository.
2. Remove the extra delete parameters across the full chain.
   - Pros: consistent contract, simpler implementation, no hidden legacy paths.
   - Cons: requires touching several files and test cleanup logic.

**Decision**
- Use approach 2.

**Behavior**
- `DELETE /VIID/ArchiveSubjects` accepts only `archive_id`.
- `ArchiveSubjectService.delete_archive_subjects`, `delete_archive_subjects_task`, and `delete_archive_subjects_repo` accept only `archive_id: str`.
- Repository deletion becomes an exact `ArchiveID` match. If found, delete and return `[archive_id]`; if not found, return `[]`.
- Test cleanup that previously relied on “all None means delete all” is rewritten to delete known sample IDs individually.

**Verification**
- Update the affected tests first so they express the new single-key contract.
- Run the targeted archive subject API/layering/e2e-facing test set to observe failures before implementation.
- Implement the minimal code changes.
- Re-run the targeted tests, `compileall`, and the full `pytest -q` suite.
