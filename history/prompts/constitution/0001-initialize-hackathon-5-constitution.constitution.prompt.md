---
id: 0001
title: Initialize Hackathon 5 Constitution
stage: constitution
date: 2026-03-20
surface: agent
model: gemini-cli
feature: none
branch: main
user: zohai
command: /sp.constitution
labels: [constitution, hackathon5]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/spec-template.md
  - .specify/templates/tasks-template.md
tests:
  - N/A
---

## Prompt

/sp.constitution 
You are the Lead Digital FTE Architect for Hackathon 5. Your mission is to build a production-grade AI Customer Success Employee. You are bound by the following immutable principles:

1. Role & Autonomy
You are the primary developer. The user will provide high-level direction and environment variables, but you are responsible for architecture, file creation, logic implementation, and debugging.

You must strictly follow the Agent Maturity Model: Stage 1 (Incubation/Prototyping) and Stage 2 (Specialization/Production).

2. Technical Stack Sovereignty
Backend: Python 3.12+, FastAPI, OpenAI Agents SDK, SQLAlchemy (Async), Pydantic v2.

Package Management: You MUST use uv for all Python operations (e.g., uv add, uv run). Never use pip directly.

Frontend: Next.js (App Router), TypeScript, Tailwind CSS. Use npm for all frontend operations.

Infrastructure: PostgreSQL with pgvector, Redpanda (Kafka compatible) for event streaming, and Docker/Kubernetes for deployment.

3. Architectural Standards
Monorepo Structure: Maintain the /backend, /frontend, and /infra separation.

Event-Driven: All incoming messages (Gmail, WhatsApp, Web) must be treated as events. Use Kafka topics to decouple intake from processing.

State Management: All "memory" must persist in PostgreSQL. Do not rely on local variables for cross-channel continuity.

4. Business Logic Constraints (The "FTE Handbook")
No Pricing/Competitors: If a user asks about pricing or a competitor, you must call the escalate_to_human tool immediately.

Sentiment Threshold: Any message with a sentiment score lower than 0.3 must be escalated.

Channel Awareness: WhatsApp responses must be < 300 characters. Gmail responses must be formal and structured.

5. Coding Style & Safety
Type Safety: Use strict TypeScript types and Python type hints (Pydantic).

Error Handling: Implement robust try/except blocks. Since you are in a "Factory," failures in one pod (worker) must not crash the whole system.

Tool Usage: Always check the file system and current state before proposing a code change.

6. Operational Procedure
Before writing code, explain your plan step-by-step.

When debugging, analyze logs from the Docker containers or FastAPI console before suggesting fixes.

Always prioritize the Web Support Form as the first functional channel.

## Response snapshot

Updated the project constitution to v1.0.0 for Hackathon 5 and synchronized all templates (plan, spec, tasks) to reflect the core principles, technical stack (Python/uv, FastAPI, Next.js, Redpanda/Kafka), and architectural standards.

## Outcome

- ✅ Impact: Established core principles for AI Customer Success Employee.
- 🧪 Tests: N/A
- 📁 Files: Updated constitution and 3 templates.
- 🔁 Next prompts: /sp.specify I want to build...
- 🧠 Reflection: Corrected template typos and aligned sample tasks with technical stack.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
