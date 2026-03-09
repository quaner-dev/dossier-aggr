# Fix Update Faces Task Test Design

**Goal:** Fix the failing task delegation test for `update_faces_task` without changing production behavior.

**Context**
- `tasks/face/face.py` calls `update_faces_repo` with a keyword argument: `update_faces_repo(faces=faces)`.
- The failing test in `tests/tasks/test_delete_tasks.py` monkeypatches `update_faces_repo` with a fake function whose parameter is named `faces_param`.
- Python matches keyword arguments by parameter name, so the fake raises `unexpected keyword argument 'faces'`.

**Approaches**
1. Fix the test double to match the production call signature.
   - Pros: minimal diff, preserves existing production API, directly addresses the failing assertion path.
   - Cons: no broader cleanup.
2. Change production code to call the repo positionally.
   - Pros: would make the current fake pass.
   - Cons: changes production style for no product benefit and risks inconsistency with the rest of the codebase.

**Decision**
- Use approach 1.

**Scope**
- Modify only `tests/tasks/test_delete_tasks.py`.
- Keep `tasks/face/face.py` unchanged.
- Do not alter route, service, or repository behavior.

**Verification**
- Re-run the existing failing targeted test first and confirm the current keyword-argument failure.
- Update the fake repo function to accept `faces`.
- Re-run the targeted test and the full `pytest -q` suite.
