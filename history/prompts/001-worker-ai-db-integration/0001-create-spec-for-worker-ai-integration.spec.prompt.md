---
id: 0001
title: Create spec for worker AI integration
stage: spec
date: 2026-04-05
surface: agent
model: gemini-2.0-flash
feature: 001-worker-ai-db-integration
branch: 001-worker-ai-db-integration
user: zohai
command: /sp.specify
labels: [spec, worker, ai, integration]
links:
  spec: specs/001-worker-ai-db-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-worker-ai-db-integration/spec.md
  - specs/001-worker-ai-db-integration/checklists/requirements.md
tests:
  - N/A
---

## Prompt

Build "Feature 4.2: Worker & DB Integration". We have a working standalone Kafka worker (app/workers/main_worker.py) and an isolated Gemini AI Agent (app/ai/agent.py). We now need to integrate the AI agent into the Kafka worker's processing loop and update the database with the results. [TECH STACK & DEPENDENCIES] - Environment: Backend only (/backend directory). - Existing Components: app.workers.main_worker, app.ai.agent.process_ticket, app.core.database.async_session_maker, app.models.ticket.Ticket. [REQUIREMENTS: THE INTEGRATION LOGIC] 1. Worker Update (main_worker.py): - Import the process_ticket function from app.ai.agent. - Inside the Kafka consumer async for msg in consumer: loop, extract the ticket payload from the message. - Pass the payload to await process_ticket(payload). 2. Database Update (Closing the Loop): - After receiving the TicketAnalysis (Pydantic object) from the AI, open an async database session using the existing async_session_maker (or dependency). - Fetch the corresponding Ticket record from the database using the ticket_id from the Kafka payload. - Update the ticket with the AI's data: - Save the suggested_response. - Save the category. - Update the ticket status to something like AI_PROCESSED or OPEN. - Commit the transaction. 3. Resilience & Error Handling: - Wrap the AI processing and Database update in a try/except block. - If the AI fails (e.g., API timeout) or the DB update fails, log the error but do not crash the worker loop. The worker must survive to process the next message. [CONSTRAINTS & RULES] - Do not modify the frontend or the FastAPI web endpoints. - Ensure the database connection is cleanly opened and closed within the processing loop to prevent connection leaks.

## Response snapshot

Successfully created specification and quality checklist for "Worker & DB Integration" in branch 001-worker-ai-db-integration. Ready for /sp.plan.

## Outcome

- ✅ Impact: High - Defines the integration path for AI and Database in the worker loop.
- 🧪 Tests: N/A - Specification phase.
- 📁 Files: Created spec.md and requirements checklist.
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: The user request was very detailed, allowing for a high-quality spec with minimal clarification.

## Evaluation notes (flywheel)

- Failure modes observed: Contradiction in system prompt about global vs short-name numbering.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
