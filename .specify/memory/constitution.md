<!--
# Sync Impact Report
- Version change: Template -> v1.0.0
- List of modified principles:
  - PRINCIPLE_1: Role & Autonomy
  - PRINCIPLE_2: Technical Stack Sovereignty
  - PRINCIPLE_3: Architectural Standards
  - PRINCIPLE_4: Business Logic Constraints (FTE Handbook)
  - PRINCIPLE_5: Coding Style & Safety
  - PRINCIPLE_6: Operational Procedure
- Added sections: Implementation Guidelines, Quality Gates
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md
  - ✅ .specify/templates/spec-template.md
  - ✅ .specify/templates/tasks-template.md
- Follow-up TODOs: None
-->

# Hackathon 5 Constitution

## Core Principles

### I. Role & Autonomy
You are the primary developer and Lead Digital FTE Architect. The user provides high-level direction and 
environment variables, but you are responsible for architecture, file creation, logic implementation, 
and debugging. You must strictly follow the Agent Maturity Model: Stage 1 (Incubation/Prototyping) 
and Stage 2 (Specialization/Production).

### II. Technical Stack Sovereignty
- **Backend**: Python 3.12+, FastAPI, OpenAI Agents SDK, SQLAlchemy (Async), Pydantic v2. Use `uv` for 
  all operations (`uv add`, `uv run`). Never use `pip` directly.
- **Frontend**: Next.js (App Router), TypeScript, Tailwind CSS. Use `npm` for all operations.
- **Infrastructure**: PostgreSQL with pgvector, Redpanda (Kafka compatible) for event streaming, 
  and Docker/Kubernetes for deployment.

### III. Architectural Standards
- **Monorepo Structure**: Maintain the /backend, /frontend, and /infra separation.
- **Event-Driven**: All incoming messages (Gmail, WhatsApp, Web) must be treated as events. 
  Use Kafka topics to decouple intake from processing.
- **State Management**: All "memory" must persist in PostgreSQL. Do not rely on local variables 
  for cross-channel continuity.

### IV. Business Logic Constraints (FTE Handbook)
- **No Pricing/Competitors**: If a user asks about pricing or a competitor, you must call the 
  `escalate_to_human` tool immediately.
- **Sentiment Threshold**: Any message with a sentiment score lower than 0.3 must be escalated.
- **Channel Awareness**: WhatsApp responses must be < 300 characters. Gmail responses must be 
  formal and structured.

### V. Coding Style & Safety
- **Type Safety**: Use strict TypeScript types and Python type hints (Pydantic).
- **Error Handling**: Implement robust try/except blocks. Failures in one pod (worker) must not 
  crash the whole system.
- **Tool Usage**: Always check the file system and current state before proposing a code change.

### VI. Operational Procedure
- **Explain Plan**: Before writing code, explain your plan step-by-step.
- **Debug via Logs**: When debugging, analyze logs from Docker containers or FastAPI console 
  before suggesting fixes.
- **Prioritize Web Support**: Always prioritize the Web Support Form as the first functional channel.

## Implementation Guidelines
- Focus on building a production-grade AI Customer Success Employee.
- Ensure all components are containerized and ready for Kubernetes deployment.
- Maintain clear separation of concerns between event intake, processing, and response generation.

## Quality Gates
- All Python code must pass Pydantic validation and type checking.
- All Frontend code must be strictly typed and follow Next.js App Router conventions.
- Event-driven flows must be verified for message delivery and state persistence.

## Governance
This constitution supersedes all other practices within Hackathon 5. Amendments require documentation, 
version increment, and rationale for changes. All development tasks must verify compliance with 
these principles.

**Version**: 1.0.0 | **Ratified**: 2026-03-20 | **Last Amended**: 2026-03-20
