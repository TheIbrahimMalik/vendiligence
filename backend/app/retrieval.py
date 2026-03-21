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

    scored: list[tuple[float, EvidenceChunk]] = []
    for chunk in evidence:
        content_tokens = _tokenize(chunk.content)
        title_tokens = _tokenize(chunk.title)
        tag_tokens = {t.lower() for t in chunk.tags}

        score = 0.0
        for token in query_tokens:
            if token in content_tokens:
                score += 1
            if token in title_tokens:
                score += 2
            if token in tag_tokens:
                score += 2

        if score > 0:
            scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [chunk for _, chunk in scored[:top_k]]
