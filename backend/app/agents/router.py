"""Router agent: classify each question as retrieve or blocked."""

from __future__ import annotations

from app.guardrails import check_prompt_injection, check_secrets
from app.models import RouterAction, RouterResult


def run(question_text: str) -> RouterResult:
    """Deterministic routing: detect malicious patterns, otherwise retrieve."""
    reasons: list[str] = []

    if check_prompt_injection(question_text):
        reasons.append("prompt injection detected")
    if check_secrets(question_text):
        reasons.append("secrets request detected")

    if reasons:
        return RouterResult(
            action=RouterAction.BLOCKED,
            reason="; ".join(reasons),
        )

    return RouterResult(
        action=RouterAction.RETRIEVE,
        reason="question is safe to process",
    )
