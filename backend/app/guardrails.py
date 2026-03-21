"""Runtime guardrail checks: secrets, prompt injection, unsupported claims."""

from __future__ import annotations

import re

from app.models import EvidenceChunk

# Patterns that indicate secrets or credentials
_SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}", re.IGNORECASE),  # AWS access key
    re.compile(r"aws.{0,10}secret.{0,10}access.{0,10}key", re.IGNORECASE),
    re.compile(r"password\s*[:=]\s*\S+", re.IGNORECASE),
    re.compile(r"api[_-]?key\s*[:=]\s*\S+", re.IGNORECASE),
    re.compile(r"token\s*[:=]\s*\S+", re.IGNORECASE),
    re.compile(r"-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----", re.IGNORECASE),
]

# Patterns that indicate prompt injection attempts
_INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?(previous\s+)?instructions", re.IGNORECASE),
    re.compile(r"(output|reveal|show|print)\s+(your\s+)?system\s+prompt", re.IGNORECASE),
    re.compile(r"disregard\s+(all\s+)?(prior|previous|above)", re.IGNORECASE),
    re.compile(r"you\s+are\s+now\s+in\s+", re.IGNORECASE),
    re.compile(r"new\s+instructions?\s*:", re.IGNORECASE),
]


def check_secrets(text: str) -> bool:
    """Return True if text appears to contain secrets or credentials."""
    return any(p.search(text) for p in _SECRET_PATTERNS)


def check_prompt_injection(text: str) -> bool:
    """Return True if text contains prompt injection patterns."""
    return any(p.search(text) for p in _INJECTION_PATTERNS)


def check_unsupported_claim(answer: str | None, citations: list[EvidenceChunk]) -> bool:
    """Return True if there is a draft answer but no supporting citations."""
    return bool(answer) and len(citations) == 0
