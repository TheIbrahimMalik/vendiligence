"""Persistent run state storage. In-memory dict by default; Postgres when DATABASE_URL is set."""

from __future__ import annotations

from app.models import RunResult

# In-memory store — keyed by run ID
_runs: dict[str, RunResult] = {}


def init_storage() -> None:
    """Initialize the storage backend. No-op for in-memory."""
    pass


def reset_storage() -> None:
    """Clear all stored data."""
    _runs.clear()


def save_run(run_result: RunResult) -> str:
    """Persist a run result and return its ID."""
    _runs[run_result.id] = run_result
    return run_result.id


def get_run(run_id: str) -> RunResult | None:
    """Retrieve a run by ID."""
    return _runs.get(run_id)
