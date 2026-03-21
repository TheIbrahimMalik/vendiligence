"""In-memory evidence retrieval using keyword overlap with title/tag boosts."""

from __future__ import annotations

import json
from pathlib import Path

from app.models import EvidenceChunk

STOPWORDS = frozenset(
    "a an the is are was were do does did have has had be been being "
    "in on at to for of and or but not with by from as it its you your "
    "we our they their this that".split()
)


def load_evidence(path: str | Path) -> list[EvidenceChunk]:
    with open(path) as f:
        raw = json.load(f)
    return [EvidenceChunk(**item) for item in raw]


def _tokenize(text: str) -> set[str]:
    tokens = set(text.lower().split())
    return tokens - STOPWORDS


def search_evidence(
    query: str,
    evidence: list[EvidenceChunk],
    top_k: int = 3,
) -> list[EvidenceChunk]:
    query_tokens = _tokenize(query)
    if not query_tokens:
        return []

    # Build document frequency: how many chunks contain each token (across all fields).
    # Tokens appearing in many chunks are less discriminating and get lower weight.
    n = len(evidence)
    doc_freq: dict[str, int] = {}
    for chunk in evidence:
        all_tokens = (
            _tokenize(chunk.content)
            | _tokenize(chunk.title)
            | {t.lower() for t in chunk.tags}
        )
        for t in all_tokens:
            doc_freq[t] = doc_freq.get(t, 0) + 1

    scored: list[tuple[float, EvidenceChunk]] = []
    for chunk in evidence:
        content_tokens = _tokenize(chunk.content)
        title_tokens = _tokenize(chunk.title)
        tag_tokens = {t.lower() for t in chunk.tags}

        score = 0.0
        for token in query_tokens:
            # Tokens that appear in fewer chunks get higher weight
            df = doc_freq.get(token, 0)
            if df == 0:
                continue
            specificity = n / df  # 1.0 when in all chunks, higher when rare

            if token in title_tokens:
                score += 3 * specificity
            if token in tag_tokens:
                score += 3 * specificity
            if token in content_tokens:
                score += 1 * specificity

        if score > 0:
            scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [chunk for _, chunk in scored[:top_k]]
