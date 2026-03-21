"""FastAPI app for Vendiligence."""

from __future__ import annotations

import json
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.agents.runner import execute_run
from app.models import EvidenceChunk, ExportResult, Question, RunResult, Status
from app.retrieval import load_evidence, search_evidence
from app.storage import get_run, init_storage, reset_storage

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _load_fixtures() -> tuple[list[EvidenceChunk], list[Question]]:
    evidence = load_evidence(DATA_DIR / "evidence.json")
    with open(DATA_DIR / "questionnaire.json") as f:
        questions = [Question(**q) for q in json.load(f)]
    return evidence, questions


@asynccontextmanager
async def lifespan(app: FastAPI):
    evidence, questions = _load_fixtures()
    app.state.evidence = evidence
    app.state.questions = questions
    init_storage()
    yield


app = FastAPI(title="Vendiligence", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Core endpoints
# ---------------------------------------------------------------------------

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/demo/load")
def demo_load(request: Request):
    """Reset state and confirm fixture counts."""
    reset_storage()
    return {
        "questions_loaded": len(request.app.state.questions),
        "evidence_loaded": len(request.app.state.evidence),
    }


@app.post("/api/runs", response_model=RunResult)
def create_run(request: Request):
    """Execute the full 3-agent pipeline and return results."""
    questions = request.app.state.questions
    evidence = request.app.state.evidence
    if not questions:
        raise HTTPException(status_code=400, detail="No questions loaded")
    return execute_run(questions, evidence)


@app.get("/api/runs/{run_id}", response_model=RunResult)
def get_run_by_id(run_id: str):
    """Retrieve a completed run by ID."""
    result = get_run(run_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return result


# ---------------------------------------------------------------------------
# MCP tool routes — exposed via fastapi-mcp as the locked toolkit
# ---------------------------------------------------------------------------

class SearchEvidenceRequest(BaseModel):
    query: str
    top_k: int = 3


@app.post("/api/tools/search_evidence")
def tool_search_evidence(request: Request, body: SearchEvidenceRequest):
    """Search approved evidence. Exposed as MCP tool via Civic hub."""
    evidence = request.app.state.evidence
    results = search_evidence(body.query, evidence, body.top_k)
    return [chunk.model_dump() for chunk in results]


class ExportPackageRequest(BaseModel):
    run_id: str


@app.post("/api/tools/export_package", response_model=ExportResult)
def tool_export_package(body: ExportPackageRequest):
    """Export answer pack. Blocked if any BLOCKED answers exist."""
    result = get_run(body.run_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Run not found")
    blocked = [a for a in result.answers if a.status == Status.BLOCKED]
    if blocked:
        raise HTTPException(
            status_code=403,
            detail=f"Export blocked: {len(blocked)} BLOCKED answer(s) present",
        )
    return ExportResult(
        run_id=body.run_id,
        exported_at=datetime.now(timezone.utc),
        answers=result.answers,
        tasks=result.tasks,
        blocked_count=0,
        export_permitted=True,
    )


# ---------------------------------------------------------------------------
# Mount fastapi-mcp — exposes tool routes as MCP-compatible endpoints
# ---------------------------------------------------------------------------

from fastapi_mcp import FastApiMCP  # noqa: E402

mcp = FastApiMCP(app, name="vendiligence-tools", describe_full_response_schema=True)
mcp.mount_http()
