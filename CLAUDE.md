# Vendiligence — CLAUDE.md

## Project Goal
Autonomous Vendor Due-Diligence Agent. Processes a vendor security questionnaire, answers from approved evidence, creates follow-up tasks for missing info, and blocks unsafe disclosures before anything is exported.

Hackathon MVP targets:
- **AI Agents track** — autonomous planning, tool use, multi-agent orchestration
- **Civic guardrails challenge** — visible runtime blocks on secrets, unsupported disclosures, prompt injection, and blocked exports

---

## Hard Constraints

| Constraint | Value |
|---|---|
| Backend | FastAPI |
| Frontend | Next.js |
| Agent runtime | OpenAI Agents SDK |
| App state | SQLite |
| Agents | Exactly 3 |
| Auth | None |
| File parsing | None (no arbitrary PDF/XLSX) |
| External integrations | None (no email, Slack, Jira) |
| Vector DB | None |
| Workflows | One main workflow only |

Demo data must be seeded first. No feature ships unless it is visible in the demo.

---

## The 3 Agents

### 1. Router Agent
- Classify each questionnaire question
- Decide: `retrieve` / `missing` / `blocked`
- Orchestrate retries on `insufficient_evidence`

### 2. Evidence Agent
- Search only approved evidence via `search_evidence` / `get_evidence_chunk`
- Draft grounded answer with citations
- Return `insufficient_evidence` when support is weak

### 3. Policy / Verifier Agent
- Verify evidence support for each draft answer
- Enforce disclosure policy
- Assign final status: `APPROVED` / `NEEDS_INFO` / `BLOCKED`

---

## Allowed Tools (never add without a concrete demo need)

| Tool | Purpose |
|---|---|
| `search_evidence` | Full-text search over approved evidence |
| `get_evidence_chunk` | Fetch a specific evidence chunk by ID |
| `create_followup_task` | Create a task for missing information |
| `save_answer` | Persist a drafted answer to SQLite |
| `log_event` | Write an audit event |
| `export_package` | Export the answer pack (blocked if any BLOCKED items exist) |

---

## Status Vocabulary
- `APPROVED` — evidence-backed, policy-cleared
- `NEEDS_INFO` — insufficient evidence, follow-up task created
- `BLOCKED` — policy violation or guardrail triggered

---

## Guardrail Requirements (must be visibly triggered in demo)
1. Secrets / credentials in a draft answer
2. Unsupported disclosures (claim without evidence)
3. Prompt injection from malicious questionnaire text
4. Export blocked when any answer is `BLOCKED`

---

## Scope Cuts (reject immediately)
- Browser automation
- Arbitrary PDF/XLSX ingestion
- Auth / multi-tenancy
- External messaging (email, Slack, Jira)
- More than 3 agents
- Long-term memory / vector DB
- Any feature not visible in the demo

---

## Preferred Build Order
1. Seed demo data (evidence + questionnaire)
2. FastAPI skeleton (routes, error handling)
3. SQLite models (questions, answers, tasks, audit events)
4. Retrieval (search_evidence, get_evidence_chunk)
5. Agent orchestration (Router → Evidence → Policy)
6. Guardrails (runtime checks at agent boundaries)
7. Audit log (log_event, trace view)
8. Evals (happy path + one critical failure path)
9. Frontend (Next.js answer pack UI)
10. Polish demo

---

## Definition of Done
The demo must show all of:
- [ ] Autonomous planning across the 3-agent pipeline
- [ ] Tool use (at minimum: search, save, log)
- [ ] Evidence-backed answers with citations
- [ ] One fallback path: `insufficient_evidence` → `NEEDS_INFO` + follow-up task
- [ ] One visible guardrail block
- [ ] Audit / trace view
- [ ] Lightweight evals (happy path + one failure path)

---

## Engineering Rules
- Simple, readable code over clever abstractions
- Deterministic behavior preferred
- Keep files small
- Tests for happy path and the one critical failure path
- Log all meaningful steps as audit events
- Keep prompts short and role-specific

## UX Rules
- Not a chatbot — the main artifact is an **answer pack** with statuses, citations, tasks, and audit events

## When in Doubt
Choose the more bounded option. A smaller polished demo beats a broader fragile system.
