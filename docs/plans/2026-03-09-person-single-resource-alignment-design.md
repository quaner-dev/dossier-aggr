# Person Single Resource Alignment Design

**Goal:** Align the `person` API module with the already-updated `face` API structure by adding single-resource update and delete routes under `/VIID/Persons/{person_id}`.

**Scope:** This change adds API endpoints and updates tests and protocol documentation. It does not change the batch `/VIID/Persons` contract or the existing service/task/repository method names, because those methods already support both single and batch operations.

**Decision:** Add two API handlers in [api/person/person.py](/root/dossier-aggr/api/person/person.py):

- `PUT /VIID/Persons/{person_id}` -> `person_update`
- `DELETE /VIID/Persons/{person_id}` -> `person_delete`

The handlers will mirror the current `face` implementation pattern in [api/face/face.py](/root/dossier-aggr/api/face/face.py): path ID is authoritative, success returns `ResponseStatus`, and the batch routes remain separate.

**Why this approach:** It keeps `person` and `face` structurally consistent, matches the protocol shape for single-resource routes, and has low implementation risk because `PersonService` already exposes `update_person` and `delete_person`.

**Validation:** Update direct API tests, HTTP contract tests, OpenAPI route registration tests, and protocol docs. Run focused `pytest` commands inside `/root/dossier-aggr-venv`; if full-suite execution is still out of scope, report the exact test subset that passed.
