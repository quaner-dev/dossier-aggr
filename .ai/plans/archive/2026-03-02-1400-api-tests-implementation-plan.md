# 1400 API Tests Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add behavior tests for all GA/T 1400 API routes currently lacking automated coverage.

**Architecture:** Keep current test style by calling route functions directly with fake services. Use minimal valid protocol models for payloads and assert response wrappers, status fields, and ID mapping consistency.

**Tech Stack:** pytest, asyncio, FastAPI route functions, SQLModel models

---

### Task 1: Add APS list route test

**Files:**
- Create: `tests/test_api_aps.py`

**Step 1:** Write failing test for `/VIID/APSs` list response shape.
**Step 2:** Run `pytest tests/test_api_aps.py -v` and verify failure.
**Step 3:** Implement minimal fake service + assertions.
**Step 4:** Run `pytest tests/test_api_aps.py -v` and verify pass.

### Task 2: Add Face route tests

**Files:**
- Create: `tests/test_api_face.py`

**Step 1:** Write failing tests for face list/by-id and create/update/delete status responses.
**Step 2:** Run `pytest tests/test_api_face.py -v` and verify failure.
**Step 3:** Implement minimal fake service + assertions.
**Step 4:** Run `pytest tests/test_api_face.py -v` and verify pass.

### Task 3: Add Person route tests

**Files:**
- Create: `tests/test_api_person.py`

**Step 1:** Write failing tests for person list/by-id and create/update/delete status responses.
**Step 2:** Run `pytest tests/test_api_person.py -v` and verify failure.
**Step 3:** Implement minimal fake service + assertions.
**Step 4:** Run `pytest tests/test_api_person.py -v` and verify pass.

### Task 4: Add Subscribe route tests

**Files:**
- Create: `tests/test_api_subscribe.py`

**Step 1:** Write failing tests for subscribe list and create/update/delete status responses.
**Step 2:** Run `pytest tests/test_api_subscribe.py -v` and verify failure.
**Step 3:** Implement minimal fake service + assertions.
**Step 4:** Run `pytest tests/test_api_subscribe.py -v` and verify pass.

### Task 5: Add SubscribeNotification route test

**Files:**
- Create: `tests/test_api_subscribe_notification.py`

**Step 1:** Write failing test for notification create status response.
**Step 2:** Run `pytest tests/test_api_subscribe_notification.py -v` and verify failure.
**Step 3:** Implement minimal fake service + assertions.
**Step 4:** Run `pytest tests/test_api_subscribe_notification.py -v` and verify pass.

### Task 6: Add Register/UnRegister/Keepalive tests

**Files:**
- Create: `tests/test_api_system.py`

**Step 1:** Write failing tests for system endpoints status responses and APS update invocation.
**Step 2:** Run `pytest tests/test_api_system.py -v` and verify failure.
**Step 3:** Implement minimal fake service + assertions.
**Step 4:** Run `pytest tests/test_api_system.py -v` and verify pass.

### Task 7: Verification

**Files:**
- Verify only

**Step 1:** Run `pytest tests/test_api_aps.py tests/test_api_face.py tests/test_api_person.py tests/test_api_subscribe.py tests/test_api_subscribe_notification.py tests/test_api_system.py -q`.
**Step 2:** Run `pytest -q`.
**Step 3:** Confirm all tests pass and no unrelated code changes were introduced.
