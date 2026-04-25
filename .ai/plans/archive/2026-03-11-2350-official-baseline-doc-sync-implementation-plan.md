# 2350 Official Baseline Doc Sync Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Align the repository's 2350 protocol documentation and protocol guard tests with the official GA/T 2350.5-2025 PDF baseline, without changing API or model behavior yet.

**Architecture:** Keep runtime behavior unchanged in this slice. Tighten the protocol guard tests first so they fail against the outdated documentation, then update `.ai/protocols/2350/README.md`, `.ai/project/README.md`, and `.ai/testing/README.md` to describe the official PDF baseline and the currently known implementation gaps.

**Tech Stack:** Markdown, pytest

---

### Task 1: Add Failing Protocol Guard Coverage For The Official 2350 Baseline

**Files:**
- Modify: `tests/protocol/test_protocol_matrix_guard.py`
- Test: `tests/protocol/test_protocol_matrix_guard.py`

**Step 1: Write the failing test**

```python
def test_protocol_2350_doc_references_official_pdf_baseline():
    content = Path(".ai/protocols/2350/README.md").read_text(encoding="utf-8")
    assert "GA-T 2350.5-2025.pdf" in content


def test_protocol_2350_doc_records_known_interface_gaps():
    content = Path(".ai/protocols/2350/README.md").read_text(encoding="utf-8")
    assert "A.9" in content and "POST" in content and "ArchiveQuery" in content
    assert "A.17" in content and "ArchiveList" in content
    assert "A.18" in content and "VehicleArchiveList" in content
```

**Step 2: Run test to verify it fails**

Run: `pytest -q tests/protocol/test_protocol_matrix_guard.py`
Expected: FAIL because `.ai/protocols/2350/README.md` still points to the deleted draft docx and does not describe the official-baseline gaps.

**Step 3: Write minimal implementation**

Update the 2350 protocol document so it:
- cites `.protocol/2350/GA-T 2350.5-2025.pdf` as the source of truth
- distinguishes official Appendix A/B requirements from current repository behavior
- explicitly records the confirmed gaps for A.9, A.13, A.15, A.17, and A.18

**Step 4: Run test to verify it passes**

Run: `pytest -q tests/protocol/test_protocol_matrix_guard.py`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/protocol/test_protocol_matrix_guard.py .ai/protocols/2350/README.md
git commit -m "docs: sync 2350 protocol baseline"
```

### Task 2: Sync Architecture And Testing Docs To The Same Baseline

**Files:**
- Modify: `.ai/project/README.md`
- Modify: `.ai/testing/README.md`
- Test: `pytest -q`

**Step 1: Write the failing test**

Use the guard test from Task 1 as the red test for the repo-wide baseline shift, then rely on full-suite verification to catch stale doc assertions after the updates.

**Step 2: Run test to verify it fails**

Run: `pytest -q tests/protocol/test_protocol_matrix_guard.py`
Expected: FAIL before the doc sync lands.

**Step 3: Write minimal implementation**

Update the architecture and testing docs so they no longer claim full A.5-A.18 alignment and instead document:
- official-baseline source is the formal PDF
- A.9/A.13/A.15/A.17/A.18 still diverge from the standard
- protocol tests are guarding documentation and known gap reporting in this slice

**Step 4: Run test to verify it passes**

Run: `pytest -q`
Expected: PASS

**Step 5: Commit**

```bash
git add .ai/project/README.md .ai/testing/README.md
git commit -m "docs: record 2350 baseline gaps"
```
