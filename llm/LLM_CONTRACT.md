# LLM Contract (Authoritative)

> This document defines how LLMs (Cursor, agents, copilots) MUST behave
> when reading, modifying, or reasoning about this repository.
> It is independent of implementation details.

## General Rules

- Prefer reading `ARCHITECTURE.md` over scanning the repository.
- Do NOT assume missing features exist.
- Do NOT invent behavior for undefined or partial components.
- When information is missing or ambiguous, FLAG it explicitly.

## Assumption Rules

- `[PLANNED]` items are design intent only and MUST NOT be treated as implemented.
- `[PARTIAL]` items may change and MUST be handled conservatively.
- Absence of code means absence of functionality.

## Modification Rules

- API layer MUST NOT access the database directly.
- Task layer MUST own its database session lifecycle.
- Cross-layer refactors REQUIRE explicit instruction.

## Risky Operations (Require Confirmation)

- Database schema changes
- Authentication or authorization changes
- Message broker or task execution changes

## Forbidden Behaviors

- Do NOT auto-complete future features.
- Do NOT refactor for stylistic reasons only.
- Do NOT normalize architecture beyond documented invariants.

## Conflict Resolution

- `ARCHITECTURE.md` overrides `ARCHITECTURE.ROADMAP.md`.
- This document overrides all others in case of behavioral conflict.

---
