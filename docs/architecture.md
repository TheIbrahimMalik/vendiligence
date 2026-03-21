# Vendiligence Architecture

## Overview

Vendiligence is a bounded autonomous workflow for vendor due-diligence questionnaires.

It processes each questionnaire item through three stages:

1. route the question
2. retrieve supporting evidence
3. verify support and policy

The final result for each question is one of:

- `APPROVED`
- `NEEDS_INFO`
- `BLOCKED`

The system is designed to make both useful automation and safe refusal visible.

## Design principles

### 1. Vertical, not general
Vendiligence is not a horizontal assistant. It handles one narrow workflow: answering vendor due-diligence questions from approved evidence.

### 2. Explicit roles
The workflow is split into three clear agents so behavior is inspectable and demoable.

### 3. Support before approval
Approved answers must be grounded in retrieved evidence.

### 4. Refusal is a real outcome
If evidence is missing, the system creates a follow-up task. If a request is malicious or unsafe, it is blocked.

### 5. Honest guardrail reporting
The system records whether it is using the Civic integration path or a local fallback, and exposes that in the audit log.

## System components

### Frontend

The frontend is a single-page Next.js dashboard.

It provides:
- Load Demo Data
- Run Questionnaire
- summary counts
- per-question results
- citations
- follow-up tasks
- audit timeline

The UI is intentionally narrow so the core workflow is obvious in a short demo.

### Backend

The backend is a FastAPI service.

Implemented endpoints:
- `POST /api/demo/load`
- `POST /api/runs`
- `GET /api/runs/{id}`
- `GET /health`

`POST /api/runs` is the central endpoint. It executes the questionnaire through the full pipeline and returns a completed run.

## Data model

The current implementation uses seeded demo fixtures:
- questionnaire
- evidence pack

Core runtime entities include:
- runs
- questions
- answers
- citations
- follow-up tasks
- audit events

These entities support both the workflow and the audit UI.

## Agent architecture

### 1. Router

**Responsibility**
Determines the initial handling path for each question.

**Inputs**
- question text

**Outputs**
A routing decision that determines whether the question should proceed through evidence retrieval, become a missing-information path, or be blocked.

**Why it matters**
The system does not retrieve blindly. It first decides how the question should be treated.

### 2. Evidence

**Responsibility**
Finds relevant approved evidence and drafts a grounded answer with citations.

**Inputs**
- question text
- approved evidence pack

**Outputs**
- draft answer
- ranked citations
- support signal

**Current implementation**
The retrieval path is deterministic and ranking-based, which keeps the demo stable, testable, and easy to inspect.

**Why it matters**
Approved answers are visibly tied to evidence instead of appearing as unsupported output.

### 3. Policy / Verifier

**Responsibility**
Decides whether a draft should be approved, turned into a follow-up task, or blocked.

**Checks**
- is the answer supported by retrieved evidence?
- does the question contain malicious instruction-following behavior?
- does the request ask for unsafe or sensitive information?

**Outputs**
- final status
- reason / notes
- follow-up task creation when needed

**Why it matters**
This stage is the boundary that makes the workflow credible rather than merely fast.

## Civic integration path and local fallback

Vendiligence includes a **Civic MCP hub integration path with local fallback**.

### Current behavior
- if Civic is configured, the backend has a dedicated integration path for Civic-backed checks
- if Civic is not configured, the workflow uses local guardrail logic
- the audit log records this honestly, including a `session_start` event

### Why this matters
The system does not pretend to be in a guardrail mode it is not using. The audit trail makes the active mode visible.

## End-to-end flow

1. Demo data is loaded
2. A run is started
3. The backend iterates through questionnaire items
4. Each question passes through:
   - Router
   - Evidence
   - Policy / Verifier
5. Audit events are recorded during execution
6. The run result is returned
7. The frontend renders:
   - summary counts
   - per-question outcomes
   - follow-up tasks
   - audit timeline

## Example outcomes in the current demo

### Approved
A supported security question is answered with retrieved evidence and citations.

### Needs info
A question with insufficient evidence is not guessed. It becomes a follow-up task.

### Blocked
A malicious question that tries to override instructions and request credentials is flagged and blocked.

These outcomes are central to the design because they show that the system is optimized for correct handling, not just answer generation.

## Guardrails model

The current implementation includes a guardrails-oriented policy layer with two visible modes:

### Civic integration path
Used when Civic is configured through the MCP hub path.

### Local fallback
Used when Civic is not configured, with the active mode reflected in the audit log.

The workflow focuses on visible guardrail-relevant cases:
- malicious instruction attempts
- unsafe disclosure requests
- unsupported answers

## Auditability

Audit events are recorded and exposed in the frontend timeline.

Typical events include:
- session start
- routing decision
- evidence retrieval
- answer approval
- follow-up task creation
- block event
- fallback mode visibility when Civic is not configured

This makes the workflow inspectable rather than opaque.

## Why this architecture works

This architecture is intentionally narrow, but strong on the dimensions that matter:

**Autonomy**
The system makes structured decisions across multiple stages.

**Usefulness**
It addresses a real enterprise bottleneck.

**Technical depth**
It demonstrates orchestration, retrieval, verification, task creation, auditability, and an honest guardrail integration boundary.

**Creativity**
It treats refusal and escalation as first-class product behaviors, not edge cases.

## Current implementation boundaries

The current version does not attempt to solve:
- arbitrary document ingestion
- generalized enterprise search
- external send workflows
- auth and multi-tenant controls

That is deliberate. The value of the demo comes from finishing one believable workflow well.
