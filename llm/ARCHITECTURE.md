# Architecture (Authoritative, State-aware)

> This document is the **single source of truth** for the current system architecture.
> It describes WHAT EXISTS TODAY.

## State Markers

- `[IMPLEMENTED]` = exists and can be relied on
- `[PARTIAL]` = exists but incomplete / unstable
- `[PLANNED]` = not implemented, design intent only

---

## 1. Purpose

### [IMPLEMENTED]

- HTTP API server implementing core VIID (GA/T 1400.4-2017)
- System: Register / UnRegister / Keepalive
- Collection: APS, APE
- Face & Person CRUD
- Subscribe & SubscribeNotification
- Async write processing via Taskiq
- SQLModel + async DB engine

### [PARTIAL]

- Archive: ArchiveLibrary, Archive, ArchiveSubject

### [PLANNED]

- Extended VIID endpoints
- Cross-entity archive queries

---

## 2. High-level Architecture

### [IMPLEMENTED]

- Entry: `main.py` (FastAPI + Taskiq app target)
- API layer: routing only, Depends(Service)
- Service layer: business logic
- Task layer: async tasks with isolated DB sessions
- Models: SQLModel + Pydantic
- Config: env-driven settings
- Alembic migrations via SQLModel metadata

### [PARTIAL]

- Service-level session injection undefined
- Mixed task vs direct DB writes

---

## 3. Invariants (Current)

- Register is the ONLY endpoint using Digest auth
- Taskiq app target is `main:app`
- DB write tasks MUST create their own AsyncSession
- URL paths MUST come from `constants.py`
- `DataNotFoundError` returns HTTP 200 with StatusCode "9"

---

## 4. What MUST NOT Be Assumed

- Planned models or endpoints exist
- get_session() is wired into DI
- Archive domain is complete

---
