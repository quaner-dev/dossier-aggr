# Person Query Align Face Design

**Goal:** Make `persons_query` behave like `faces_query`: no API-side filter parameters, and batch query returns the first fixed-size page from the repository.

**Scope:** This change affects the `GET /VIID/Persons` behavior, its backing repository query, targeted tests, and protocol documentation. Single-person routes and batch write routes remain unchanged.

**Decision:** Align `person` query behavior with `face` in two places:

- [api/person/person.py](/root/dossier-aggr/api/person/person.py): remove `person_ids` / `source_id` / `device_id` query parameters and API-side filtering from `persons_query`
- [repo/person/person.py](/root/dossier-aggr/repo/person/person.py): order by `PersonID` and return a fixed-size default list, matching the `face` repository pattern

**Recommended approach:** Use the same default page size as `face` (`100`) and let an empty query return an empty list rather than raising `DataNotFoundError`. This keeps `person` and `face` query semantics consistent and removes unnecessary divergence in the read path.

**Alternatives considered:**

- Remove only API-side filters but keep repository returning all rows: simpler, but does not actually align with the fixed-size list behavior
- Keep filters and only add a limit: rejected because the user explicitly asked for `face`-style behavior

**Validation:** Update the HTTP contract test so query params no longer filter results, then run targeted `pytest` commands and syntax compilation. Update `.docs` to reflect that `GET /VIID/Persons` returns the default top list instead of supporting query filters.
