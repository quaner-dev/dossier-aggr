# Subscribe Notification Protocol Correction Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace the incorrect single-notification query implementation with protocol-aligned batch query and delete behavior on `/VIID/SubscribeNotifications`.

**Architecture:** The query path becomes a synchronous `api -> service -> repository` read on the collection resource. The delete path becomes a batch write `api -> service -> task -> repository`, matching the existing layering pattern used elsewhere in the codebase. Package exports and docs are updated so the whole codebase consistently reflects the corrected contract.

**Tech Stack:** Python, FastAPI, SQLModel, Taskiq, pytest

---

### Task 1: Express the corrected contract in tests

**Files:**
- Modify: `tests/test_api_subscribe_notification.py`
- Modify: `tests/services/test_subscribe_layering.py`
- Modify: `tests/protocol/test_1400_routes.py`
- Modify: `tests/protocol/test_2350_routes.py`

**Step 1: Write the failing tests**

Update tests to expect:
- `subscribe_notifications_query`
- `subscribe_notifications_delete`
- no `/VIID/SubscribeNotifications/{notification_id}` route

**Step 2: Run test to verify it fails**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/test_api_subscribe_notification.py tests/services/test_subscribe_layering.py tests/protocol/test_1400_routes.py tests/protocol/test_2350_routes.py -q`
Expected: FAIL because the implementation still exposes the single-resource query path.

**Step 3: Write minimal implementation**

Update API/service/task/repository and package exports for batch query/delete only.

**Step 4: Run tests to verify they pass**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest tests/test_api_subscribe_notification.py tests/services/test_subscribe_layering.py tests/protocol/test_1400_routes.py tests/protocol/test_2350_routes.py -q`
Expected: PASS

**Step 5: Sync docs**

Update:
- `.docs/PROTOCOL_1400.md`
- `.docs/PROTOCOL_2350.md`
- `.docs/ARCHITECTURE.md`
- `.docs/TESTING.md`

**Step 6: Run broader verification**

Run: `source /root/dossier-aggr-venv/bin/activate && pytest -q`
Expected: PASS

**Step 7: Verify syntax**

Run: `source /root/dossier-aggr-venv/bin/activate && python -m compileall api/subscribe/subscribe_notification.py services/subscribe/subscribe_notification.py tasks/subscribe/subscribe_notification.py repo/subscribe/subscribe_notification.py tests/test_api_subscribe_notification.py tests/services/test_subscribe_layering.py tests/protocol/test_1400_routes.py tests/protocol/test_2350_routes.py`
Expected: PASS
