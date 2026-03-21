"""Pydantic models for the Vendiligence run flow."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Status(str, Enum):
    APPROVED = "APPROVED"
    NEEDS_INFO = "NEEDS_INFO"
    BLOCKED = "BLOCKED"
    PENDING = "PENDING"


class RouterAction(str, Enum):
    RETRIEVE = "retrieve"
    BLOCKED = "blocked"


class Question(BaseModel):
    id: str
    text: str
    category: str


class EvidenceChunk(BaseModel):
    id: str
    source_doc: str
    title: str
    tags: list[str]
    content: str


class Answer(BaseModel):
    question_id: str
    question_text: str
    status: Status
    draft_answer: Optional[str] = None
    citations: list[EvidenceChunk] = Field(default_factory=list)
    reason: str = ""


class FollowupTask(BaseModel):
    id: str
    run_id: str
    question_id: str
    description: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AuditEvent(BaseModel):
    id: str
    run_id: str
    question_id: str
    agent: str
    action: str
    detail: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class RunResult(BaseModel):
    id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    civic_session_id: Optional[str] = None
    answers: list[Answer] = Field(default_factory=list)
    tasks: list[FollowupTask] = Field(default_factory=list)
    audit_events: list[AuditEvent] = Field(default_factory=list)


class ExportResult(BaseModel):
    run_id: str
    exported_at: datetime
    answers: list[Answer] = Field(default_factory=list)
    tasks: list[FollowupTask] = Field(default_factory=list)
    blocked_count: int = 0
    export_permitted: bool = True


class RouterResult(BaseModel):
    action: RouterAction
    reason: str


class EvidenceResult(BaseModel):
    draft_answer: Optional[str] = None
    citations: list[EvidenceChunk] = Field(default_factory=list)
    confidence: float = 0.0
    sufficient: bool = False


class PolicyResult(BaseModel):
    status: Status
    reason: str
    task: Optional[FollowupTask] = None
