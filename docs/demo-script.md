# Vendiligence Demo Script

## Goal

Show a clear 3-minute story:

- this is a real problem
- the workflow is autonomous
- the output is useful
- the system handles missing information correctly
- the system blocks malicious requests
- the audit trail makes guardrail behavior visible

## Demo narrative in one sentence

Vendiligence automates vendor due-diligence questionnaires by answering supported questions from approved evidence, creating follow-up tasks for missing information, and blocking malicious or unsafe requests.

## 3-minute script

### 0:00 - 0:20 — Problem

"Enterprise sales teams constantly receive security questionnaires. They are repetitive, slow, and risky to automate badly. A generic assistant might guess, overclaim, or follow malicious instructions embedded in the questionnaire itself."

### 0:20 - 0:40 — Product

"Vendiligence is a bounded autonomous agent for that workflow. It routes each question, retrieves approved evidence, drafts supported answers, creates follow-up tasks when evidence is missing, and blocks malicious or unsafe requests."

Show the main dashboard.

### 0:40 - 0:55 — Load the demo

Click **Load Demo Data**.

"This demo uses a seeded questionnaire and evidence pack so the workflow is stable, repeatable, and easy to inspect."

### 0:55 - 1:30 — Run the questionnaire

Click **Run Questionnaire**.

"Each question goes through a 3-agent pipeline:
first the Router decides how to handle it,
then the Evidence agent retrieves support and drafts an answer,
and finally the Policy / Verifier decides whether it is approved, needs follow-up, or should be blocked."

Point to the summary counts:
- 3 Approved
- 1 Needs Info
- 1 Blocked

"This one run shows all three important outcomes."

### 1:30 - 1:55 — Show an approved answer

Open an approved item.

"This is an approved answer. It includes both the response and the supporting citation. The key point is that it is not just generated text — it is grounded in retrieved evidence."

Point to the citation.

"That makes the answer more credible and reviewable."

### 1:55 - 2:20 — Show the missing-information case

Open the `NEEDS_INFO` item and then the task panel.

"This question does not have enough supporting evidence in the approved pack. Vendiligence does not guess. It marks the item as needs info and creates a follow-up task."

Pause here.

"This is one of the most important behaviors in the system: uncertainty becomes an action, not a hallucination."

### 2:20 - 2:45 — Show the blocked malicious case

Open the `BLOCKED` item.

"This question is intentionally malicious. It tries to override instructions and asks for sensitive information. Vendiligence flags it and blocks it."

Pause here again. This is the strongest safety moment.

"The product story is not just that the agent can answer questions. It is that it knows what should never be answered."

### 2:45 - 3:00 — Show the audit timeline and close

Point to the audit timeline.

"The audit trail shows the workflow step by step, including session start, routing, evidence retrieval, task creation, and the block event. If Civic is not configured, the fallback path is shown honestly in the log."

Closing line:

"Vendiligence shows a practical pattern for enterprise agents: answer from evidence, escalate uncertainty, and block unsafe behavior by default."

## What to emphasize

### Most important points
- 3-agent workflow
- approved answers have citations
- missing info becomes a task
- malicious prompt is blocked
- audit trail shows what happened
- Civic mode vs local fallback is reported honestly

### Good phrases to reuse
- "bounded autonomous workflow"
- "answer what is supported"
- "create tasks for what is missing"
- "block what should never be answered"
- "honest guardrail reporting"

## What not to say

Avoid:
- claiming fully live Civic-backed enforcement if you have not verified it end-to-end
- describing the product as a generic assistant
- spending too long on framework choices
- talking about future integrations

Keep the story centered on what is already real in the product.

## Live demo checklist

Before presenting:
- confirm backend is running
- confirm frontend loads
- click Load Demo Data
- click Run Questionnaire
- verify counts show:
  - 3 APPROVED
  - 1 NEEDS_INFO
  - 1 BLOCKED
- confirm one follow-up task is visible
- confirm blocked case is visible
- confirm audit timeline is populated
- confirm the audit shows session start and whether the run used fallback mode
