"""Tests for the questionnaire run flow."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(autouse=True)
def client():
    """Provide a test client with lifespan context, reset state before each test."""
    with TestClient(app) as c:
        c.post("/api/demo/load")
        yield c


def test_demo_load(client):
    resp = client.post("/api/demo/load")
    assert resp.status_code == 200
    data = resp.json()
    assert data["questions_loaded"] == 5
    assert data["evidence_loaded"] == 6


def test_full_run_statuses(client):
    resp = client.post("/api/runs")
    assert resp.status_code == 200
    data = resp.json()

    statuses = [a["status"] for a in data["answers"]]
    assert statuses.count("APPROVED") == 3
    assert statuses.count("NEEDS_INFO") == 1
    assert statuses.count("BLOCKED") == 1


def test_approved_answers_have_citations(client):
    resp = client.post("/api/runs")
    data = resp.json()

    for answer in data["answers"]:
        if answer["status"] == "APPROVED":
            assert len(answer["citations"]) > 0, (
                f"APPROVED answer for {answer['question_id']} has no citations"
            )
            assert answer["draft_answer"] is not None


def test_needs_info_has_followup_task(client):
    resp = client.post("/api/runs")
    data = resp.json()

    needs_info = [a for a in data["answers"] if a["status"] == "NEEDS_INFO"]
    assert len(needs_info) == 1

    task_question_ids = {t["question_id"] for t in data["tasks"]}
    assert needs_info[0]["question_id"] in task_question_ids


def test_blocked_question_has_audit_event(client):
    resp = client.post("/api/runs")
    data = resp.json()

    blocked = [a for a in data["answers"] if a["status"] == "BLOCKED"]
    assert len(blocked) == 1
    blocked_qid = blocked[0]["question_id"]

    guardrail_events = [
        e for e in data["audit_events"]
        if e["question_id"] == blocked_qid and e["agent"] == "policy"
    ]
    assert len(guardrail_events) > 0
    assert "Guardrail" in guardrail_events[0]["detail"]


def test_audit_events_per_question(client):
    resp = client.post("/api/runs")
    data = resp.json()

    question_ids = {a["question_id"] for a in data["answers"]}
    for qid in question_ids:
        events = [e for e in data["audit_events"] if e["question_id"] == qid]
        # Each question should have at least 3 events: router, evidence, policy
        assert len(events) >= 3, f"Question {qid} has only {len(events)} audit events"


def test_get_run_by_id(client):
    resp = client.post("/api/runs")
    run_id = resp.json()["id"]

    resp2 = client.get(f"/api/runs/{run_id}")
    assert resp2.status_code == 200
    assert resp2.json()["id"] == run_id


def test_get_run_not_found(client):
    resp = client.get("/api/runs/nonexistent")
    assert resp.status_code == 404


def test_encryption_question_ranks_encryption_chunk_first(client):
    """The encryption question should cite the Encryption at Rest chunk first."""
    resp = client.post("/api/runs")
    data = resp.json()

    q1 = next(a for a in data["answers"] if a["question_id"] == "q-1")
    assert q1["status"] == "APPROVED"
    assert q1["citations"][0]["id"] == "ev-1"
    assert "Encryption" in q1["citations"][0]["title"]


# ---------------------------------------------------------------------------
# Civic integration tests
# ---------------------------------------------------------------------------


def test_tool_search_evidence(client):
    """MCP tool route returns evidence chunks for a query."""
    resp = client.post("/api/tools/search_evidence", json={"query": "encryption"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 0
    assert data[0]["id"] == "ev-1"


def test_tool_export_blocked(client):
    """Export is blocked when run contains BLOCKED answers."""
    run_resp = client.post("/api/runs")
    run_id = run_resp.json()["id"]

    resp = client.post("/api/tools/export_package", json={"run_id": run_id})
    assert resp.status_code == 403
    assert "BLOCKED" in resp.json()["detail"]


def test_tool_export_succeeds(client):
    """Export succeeds when run has no BLOCKED answers (uses storage directly)."""
    from datetime import datetime, timezone
    from app.models import Answer, RunResult, Status
    from app.storage import save_run

    clean_run = RunResult(
        id="clean-test-run",
        created_at=datetime.now(timezone.utc),
        answers=[
            Answer(
                question_id="q-1",
                question_text="Test?",
                status=Status.APPROVED,
                draft_answer="Yes.",
                reason="test",
            )
        ],
    )
    save_run(clean_run)

    resp = client.post("/api/tools/export_package", json={"run_id": "clean-test-run"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["export_permitted"] is True
    assert data["blocked_count"] == 0


def test_civic_session_event(client):
    """First audit event in a run is the civic session_start event."""
    resp = client.post("/api/runs")
    data = resp.json()
    first_event = data["audit_events"][0]
    assert first_event["agent"] == "civic"
    assert first_event["action"] == "session_start"
    assert "fallback" in first_event["detail"]  # no CIVIC_TOKEN in tests
