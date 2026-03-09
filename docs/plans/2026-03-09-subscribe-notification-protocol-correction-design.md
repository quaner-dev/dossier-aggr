# Subscribe Notification Protocol Correction Design

**Goal:** Correct the `SubscribeNotification` implementation so it matches GA/T 1400.4-2017 7.2.21.2: batch query and batch delete on `/VIID/SubscribeNotifications`, with no single-resource query route.

**Scope**
- Modify `api/subscribe/subscribe_notification.py`.
- Modify `services/subscribe/subscribe_notification.py`.
- Modify `tasks/subscribe/subscribe_notification.py`.
- Modify `repo/subscribe/subscribe_notification.py`.
- Update package exports in `tasks/__init__.py` and `repo/subscribe/__init__.py`.
- Update tests in `tests/test_api_subscribe_notification.py`, `tests/services/test_subscribe_layering.py`, `tests/protocol/test_1400_routes.py`, and `tests/protocol/test_2350_routes.py`.
- Update `.docs/PROTOCOL_1400.md`, `.docs/PROTOCOL_2350.md`, `.docs/ARCHITECTURE.md`, and `.docs/TESTING.md`.

**Approaches**
1. Minimal correction: remove the single route, add batch `GET` and `DELETE`, and support batch query on top-level query-string attributes.
   - Pros: aligns with protocol shape, keeps the implementation small, and preserves layered boundaries.
   - Cons: query filtering remains limited to filterable top-level fields rather than every nested property.
2. Full generic protocol query engine for every `SubscribeNotification` attribute.
   - Pros: closest possible interpretation of “属性键-值对”.
   - Cons: much larger change with poor payoff for the current gap.

**Decision**
- Use approach 1.

**Behavior**
- Remove `GET /VIID/SubscribeNotifications/{notification_id}`.
- Add `GET /VIID/SubscribeNotifications` returning `SubscribeNotificationListSchema`.
- Add `DELETE /VIID/SubscribeNotifications` accepting `IDList` and returning `ResponseStatusListSchema`.
- Batch query passes request query parameters through to the repository as top-level filters.
- Batch delete uses a write path through `service -> task -> repository`.

**Verification**
- Rewrite the API, layering, and route tests first to the target contract.
- Run the targeted tests to observe the expected failures before implementation.
- Implement the minimal code changes.
- Re-run the targeted tests, `compileall`, and the full `pytest -q` suite.
