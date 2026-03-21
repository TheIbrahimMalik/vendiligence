"""Policy / Verifier agent: verify support, enforce policy, assign final status."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.guardrails import check_secrets, check_unsupported_claim
from app.models import (
    EvidenceResult,
    FollowupTask,
    PolicyResult,
    RouterAction,
    RouterResult,
    Status,
)


def run(
    question_id: str,
    question_text: str,
    router_result: RouterResult,
    evidence_result: EvidenceResult,
    run_id: str,
) -> PolicyResult:
    """Assign APPROVED / NEEDS_INFO / BLOCKED based on evidence and guardrails."""

    # Blocked by router
    if router_result.action == RouterAction.BLOCKED:
        return PolicyResult(
            status=Status.BLOCKED,
            reason=f"Guardrail: {router_result.reason}",
        )

    # Insufficient evidence
    if not evidence_result.sufficient:
        task = FollowupTask(
            id=str(uuid.uuid4()),
            run_id=run_id,
            question_id=question_id,
            description=f"Provide evidence for: {question_text}",
            created_at=datetime.now(timezone.utc),
        )
        return PolicyResult(
            status=Status.NEEDS_INFO,
            reason="Insufficient evidence to answer this question",
            task=task,
        )

    # Check draft answer for secrets leakage
    if evidence_result.draft_answer and check_secrets(evidence_result.draft_answer):
        return PolicyResult(
            status=Status.BLOCKED,
            reason="Guardrail: draft answer contains potential secrets",
        )

    # Check for unsupported claims
    if check_unsupported_claim(evidence_result.draft_answer, evidence_result.citations):
        return PolicyResult(
            status=Status.BLOCKED,
            reason="Guardrail: answer makes claims without supporting citations",
        )

    return PolicyResult(
        status=Status.APPROVED,
        reason=f"Supported by {len(evidence_result.citations)} evidence chunk(s)",
    )
