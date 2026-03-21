"""FastAPI app for Vendiligence."""

from __future__ import annotations

import json
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from app.agents.runner import execute_run
from app.models import EvidenceChunk, Question, RunResult
from app.retrieval import load_evidence
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
