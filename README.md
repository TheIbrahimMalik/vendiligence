# Vendiligence

**Vendiligence** is an autonomous vendor due-diligence agent for startups selling to enterprise.

It takes a security questionnaire, routes each question through a bounded 3-agent workflow, answers from approved evidence, creates follow-up tasks when evidence is missing, and blocks malicious or unsafe requests before they become answers.

This repo contains a working end-to-end demo with a FastAPI backend and a Next.js frontend.

## What it does

Vendiligence demonstrates a narrow, high-value workflow:

- load seeded demo data
- run a questionnaire through a 3-agent pipeline
- produce per-question outcomes:
  - `APPROVED`
  - `NEEDS_INFO`
  - `BLOCKED`
- include citations for approved answers
- create follow-up tasks for missing information
- record an audit timeline of key decisions
- include a Civic MCP hub integration path with local fallback

The current seeded demo produces:

- **3 APPROVED**
- **1 NEEDS_INFO**
- **1 BLOCKED**

## Why this matters

Enterprise sales teams regularly face security and due-diligence questionnaires. The process is repetitive, slow, and risky to automate poorly.

A generic assistant may:
- hallucinate unsupported claims
- miss missing evidence
- follow malicious instructions embedded in the questionnaire
- surface unsafe content with too little reviewability

Vendiligence is designed around a stricter principle:

**answer what is supported, create tasks for what is missing, and block what should never be answered.**

## Why it is agentic

Vendiligence is not a general chat assistant. It is a bounded workflow with explicit roles.

### 1. Router
Classifies each question and decides how it should be handled.

### 2. Evidence
Searches the approved evidence pack, ranks relevant evidence, and drafts grounded answers with citations.

### 3. Policy / Verifier
Checks support, enforces safety rules, and produces the final outcome.

This produces visible workflow behavior rather than one opaque model response.

## Why the blocked case is central

The demo includes a malicious questionnaire item that attempts to:
- override instructions
- extract internal prompt material
- request sensitive credentials

Vendiligence flags and blocks it.

That blocked case is not a side detail. It is central to the product story:
**the system is useful because it is autonomous, and credible because it refuses unsafe behavior.**

## Why the follow-up task is central

The demo also includes a question without enough supporting evidence.

Vendiligence does not guess. It marks the item as `NEEDS_INFO` and creates a follow-up task instead.

That behavior is a feature:
- it preserves trust
- it keeps the workflow moving
- it makes uncertainty actionable

## Civic integration status

Vendiligence includes a **Civic MCP hub integration path with transparent local fallback**.

Current status:
- Civic MCP hub integration path implemented in `backend/app/civic_tools.py`
- public MCP tool surface validated (`search_evidence`, `export_package` exposed via fastapi-mcp)
- demo runs in local fallback mode — custom remote toolkit registration was not self-serve in the current Civic environment
- audit log records the active mode honestly, including a `session_start` event on every run

The fallback is not a gap. The guardrail behaviors — blocked malicious prompt, gated export, follow-up task creation — are real and visible in every demo run.

## Current implementation

### Frontend
- Next.js single-page dashboard

### Backend
- FastAPI API
- deterministic 3-agent pipeline
- seeded questionnaire and evidence pack
- run retrieval route and Civic MCP tool boundary
- audit event recording
- Civic integration path with local fallback

### Demo flow
- `POST /api/demo/load`
- `POST /api/runs`
- `GET /api/runs/{id}`

## UI overview

The dashboard shows:
- demo controls:
  - Load Demo Data
  - Run Questionnaire
- summary counts
- per-question results
- citations for approved answers
- generated follow-up tasks
- audit timeline

The UI is intentionally simple so the core workflow is understandable in a short live demo.

## Repository structure

```text
backend/
  app/
    agents/
    main.py
    models.py
    storage.py
    guardrails.py
  data/
    evidence.json
    questionnaire.json
  tests/

frontend/
  app/
  components/
  lib/

docs/
  architecture.md
  demo-script.md
  pitch-deck-outline.md
```

## API endpoints

### POST /api/demo/load

Seeds or resets the demo questionnaire and evidence pack.

### POST /api/runs

Executes the questionnaire through the full pipeline and returns the completed run.

### GET /api/runs/{id}

Retrieves a completed run.

### GET /health

Liveness check.

## Testing

The backend test suite currently verifies the main workflow, including:

- correct per-question outcomes
- citations on approved answers
- follow-up task creation for missing evidence
- blocked malicious prompt handling
- audit event recording
- Civic session start / fallback path visibility

Current status: 13/13 tests passing

## What is intentionally out of scope

This prototype is deliberately narrow. It does not include:

- arbitrary document upload
- generic chat UX
- external sending workflows
- email integrations
- auth
- broad enterprise search

That scope discipline is intentional. The goal is a polished, believable vertical slice.

## Core takeaway

Vendiligence demonstrates a practical enterprise agent pattern:

- autonomous enough to save time
- bounded enough to trust
- transparent enough to audit
- honest about its guardrail mode
