"""Evidence agent: search approved evidence and draft an answer with citations."""

from __future__ import annotations

from app import civic_tools
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

    matches = _search(question_text, evidence_store)

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


def _search(query: str, evidence_store: list[EvidenceChunk]) -> list[EvidenceChunk]:
    """Route evidence search through Civic MCP hub or fall back to local."""
    if civic_tools.is_configured():
        try:
            raw = civic_tools.call_tool("search_evidence", {"query": query})
            return [EvidenceChunk(**c) for c in raw]
        except Exception:
            pass  # Civic hub unreachable — fall back to local
    return search_evidence(query, evidence_store, top_k=3)
