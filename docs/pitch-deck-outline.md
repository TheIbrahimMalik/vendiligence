# Vendiligence Pitch Deck Outline

## Slide 1 — Title
**Vendiligence**
Autonomous vendor due-diligence agent

Subtitle:
Answer supported questions, create follow-up tasks for missing information, and block unsafe requests.

## Slide 2 — Problem
Enterprise sales teams lose time and trust on security questionnaires.

Pain points:
- repetitive manual work
- slow deal cycles
- risky automation with generic AI
- unsupported or unsafe answers can create real problems

Core tension:
**speed vs trust**

## Slide 3 — Solution
Vendiligence is a bounded autonomous workflow for vendor due diligence.

It:
- routes each question
- retrieves approved evidence
- drafts grounded answers with citations
- creates follow-up tasks when evidence is missing
- blocks malicious or unsafe requests

Key line:
**Useful by default. Safe by design.**

## Slide 4 — Why it is agentic
3-agent pipeline:

- **Router**
  decides how the question should be handled

- **Evidence**
  finds support and drafts an answer

- **Policy / Verifier**
  approves, defers, or blocks

Key message:
This is not one model response. It is a structured decision workflow.

## Slide 5 — Demo result
Single run outcome:

- **3 APPROVED**
- **1 NEEDS_INFO**
- **1 BLOCKED**

Show:
- one approved answer with citation
- one follow-up task
- one blocked malicious prompt

Key message:
The system does not just answer. It handles uncertainty and adversarial input correctly.

## Slide 6 — Guardrails and auditability
Guardrail story:
- Civic MCP hub integration path implemented with public MCP tool surface validated
- demo runs in transparent local fallback mode — recorded honestly in the audit log
- blocked malicious case is visible and auditable in the run
- export is blocked when any answer is BLOCKED

Key message:
The workflow is inspectable. Guardrail behavior is real, visible, and not overclaimed.

## Slide 7 — Why it stands out
What judges should remember:

- **Autonomy:** structured 3-agent pipeline making real decisions at each stage
- **Usefulness:** addresses a real, repetitive enterprise bottleneck
- **Technical depth:** routing, retrieval, verification, follow-up tasks, audit log, Civic MCP tool boundary
- **Creativity:** refusal and escalation are first-class product behaviors, not edge cases
- **Guardrails/safety:** malicious prompt blocked, export gated, fallback mode reported honestly in the audit trail

Closing line:
**Vendiligence turns due-diligence automation from a risky assistant into a bounded, inspectable agent workflow.**
