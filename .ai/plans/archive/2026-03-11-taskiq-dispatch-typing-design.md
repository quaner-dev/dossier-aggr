# Taskiq Dispatch Typing Design

**Goal:** Fix the static typing of `dispatch_and_wait` so Taskiq-decorated async tasks are inferred as returning their awaited payload type `T`, not `Coroutine[..., T]`.

**Context**
- `services/task_dispatch.py` exposes `dispatch_and_wait` as the common helper for waiting on Taskiq task results.
- Taskiq decorates `async def` tasks as `AsyncTaskiqDecoratedTask[..., Coroutine[..., T]]`, and its `kiq` overload then unwraps that payload type internally.
- Our helper currently accepts `AsyncTaskiqDecoratedTask[Any, _ReturnType]` directly, so static analyzers can bind `_ReturnType` to `Coroutine[..., T]` instead of the final task result.
- The user requested a focused fix for this Taskiq coroutine inference issue only. Return-type mismatches like `Sequence[...]` vs `list[...]` stay out of scope for this change.

**Approaches**
1. Adjust `dispatch_and_wait` typing to accept both plain task return types and coroutine-wrapped task return types, while always returning the awaited payload type.
   - Pros: minimal production diff, fixes the shared helper once, keeps all call sites unchanged.
   - Cons: requires a small amount of typing boilerplate.
2. Add `cast(...)` at each service call site.
   - Pros: fast local suppression.
   - Cons: duplicates the workaround and leaves the helper incorrectly typed.
3. Wrap every Taskiq task in a project-local typed adapter.
   - Pros: explicit at each boundary.
   - Cons: unnecessary indirection and larger diff for a narrow typing issue.

**Decision**
- Use approach 1.

**Scope**
- Modify `services/task_dispatch.py` typing only.
- Add or update focused tests in `tests/services/test_task_dispatch.py`.
- Do not change Taskiq library code.
- Do not change business service signatures such as `list[...]` vs `Sequence[...]`.

**Verification**
- Add a targeted test that exercises `dispatch_and_wait` with an async Taskiq-decorated task and confirms the runtime contract still returns the final value.
- Run the targeted `tests/services/test_task_dispatch.py` tests first.
- Then attempt `pytest -q` per repository policy and report whether failures are related or pre-existing.
