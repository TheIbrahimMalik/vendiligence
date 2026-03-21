"""Evidence agent: search approved evidence and draft an answer with citations."""

from __future__ import annotations

from app.models import EvidenceChunk, EvidenceResult, RouterAction, RouterResult
from app.retrieval import search_evidence

CONFIDENCE_THRESHOLD = 0.3


def run(
    question_text: str,
    router_result: RouterResult,
    evidence_store: list[EvidenceChunk],
) -> EvidenceResult:
    """Search evidence and draft an answer. Skip if router blocked the question."""
    if router_result.action == RouterAction.BLOCKED:
        return EvidenceResult(sufficient=False)

    matches = search_evidence(question_text, evidence_store, top_k=3)

    if not matches:
        return EvidenceResult(
            draft_answer=None,
            citations=[],
            confidence=0.0,
            sufficient=False,
        )

    top = matches[0]
    draft = f"Based on our {top.source_doc} — {top.title}: {top.content}"
    confidence = min(1.0, len(matches) * CONFIDENCE_THRESHOLD + 0.2)

    return EvidenceResult(
        draft_answer=draft,
        citations=matches,
        confidence=confidence,
        sufficient=True,
    )
