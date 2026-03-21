"""Orchestrator: run Router → Evidence → Policy for each question."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app import civic_tools
from app.agents import evidence as evidence_agent
from app.agents import policy as policy_agent
from app.agents import router as router_agent
from app.models import Answer, AuditEvent, EvidenceChunk, Question, RunResult, Status
from app.storage import save_run


def _audit(
    run_id: str,
    question_id: str,
    agent: str,
    action: str,
    detail: str,
) -> AuditEvent:
    return AuditEvent(
        id=str(uuid.uuid4()),
        run_id=run_id,
        question_id=question_id,
        agent=agent,
        action=action,
        detail=detail,
        created_at=datetime.now(timezone.utc),
    )


def execute_run(
    questions: list[Question],
    evidence_store: list[EvidenceChunk],
) -> RunResult:
    """Run the full 3-agent pipeline for every question and persist the result."""
    run_id = str(uuid.uuid4())
    answers: list[Answer] = []
    tasks = []
    events: list[AuditEvent] = []

    # --- Civic session event ---
    info = civic_tools.session_info()
    if info["civic_configured"]:
        civic_detail = f"toolkit={info['toolkit']}, hub={info['hub_url']}"
    else:
        civic_detail = "civic not configured, using local fallback"
    events.append(_audit(run_id, "*", "civic", "session_start", civic_detail))

    for q in questions:
        # --- Router ---
        router_result = router_agent.run(q.text)
        events.append(
            _audit(run_id, q.id, "router", router_result.action.value, router_result.reason)
        )

        # --- Evidence ---
        ev_result = evidence_agent.run(q.text, router_result, evidence_store)
        ev_source = "civic_tool_call" if civic_tools.is_configured() else "local_search"
        ev_detail = (
            f"source={ev_source}, sufficient={ev_result.sufficient}, "
            f"citations={len(ev_result.citations)}, confidence={ev_result.confidence:.2f}"
        )
        events.append(_audit(run_id, q.id, "evidence", ev_source, ev_detail))

        # --- Policy ---
        pol_result = policy_agent.run(q.id, q.text, router_result, ev_result, run_id)
        events.append(
            _audit(run_id, q.id, "policy", pol_result.status.value, pol_result.reason)
        )

        # Assemble answer
        answer = Answer(
            question_id=q.id,
            question_text=q.text,
            status=pol_result.status,
            draft_answer=ev_result.draft_answer,
            citations=ev_result.citations,
            reason=pol_result.reason,
        )
        answers.append(answer)

        if pol_result.task:
            tasks.append(pol_result.task)

    result = RunResult(
        id=run_id,
        created_at=datetime.now(timezone.utc),
        answers=answers,
        tasks=tasks,
        audit_events=events,
    )

    save_run(result)
    return result
